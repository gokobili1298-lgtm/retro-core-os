import pygame
import random
import math
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, CYAN, NEON_PINK, NEON_YELLOW

def run_game(screen, clock, username="Kahraman"):
    running = True
    mode = "STORY_INTRO"
    
    tile_map = [
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,1,0,0,6,0,0,1,0,0,0,5,1],
        [1,0,1,0,1,0,1,1,1,0,1,0,1,1,1,1],
        [1,0,1,0,0,0,0,2,1,0,7,0,0,0,0,1],
        [1,0,1,1,1,1,0,1,1,1,1,0,1,1,0,1],
        [1,0,4,0,0,1,0,0,6,0,1,0,3,1,0,1],
        [1,1,1,1,0,1,1,1,1,0,1,1,1,1,0,1],
        [1,3,0,1,0,7,0,3,1,0,4,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    ]
    
    TILE_SIZE = 48
    offset_x = (SCREEN_WIDTH - (len(tile_map[0]) * TILE_SIZE)) // 2
    offset_y = 65
    
    player_x, player_y = 1, 1
    hero = {
        "name": username,
        "health": 100,
        "max_hp": 100,
        "gold": 0,
        "attack": 25,
        "weapon": "Afsunlu Çelik Kılıç"
    }
    
    active_question = None
    selected_answer = 0
    dialogue_title = ""
    dialogue_text = ""
    
    font_title = pygame.font.SysFont("Courier", 22, bold=True)
    font_text = pygame.font.SysFont("Courier", 15, bold=True)
    font_hud = pygame.font.SysFont("Courier", 15, bold=True)
    
    move_delay = 0
    anim_timer = 0
    
    # --- DOKUNMATİK BUTONLAR (SORUNSUZ OKLAR VE YERLEŞİM) ---
    btn_up = pygame.Rect(SCREEN_WIDTH - 140, SCREEN_HEIGHT - 160, 55, 45)
    btn_down = pygame.Rect(SCREEN_WIDTH - 140, SCREEN_HEIGHT - 105, 55, 45)
    btn_left = pygame.Rect(SCREEN_WIDTH - 200, SCREEN_HEIGHT - 132, 55, 45)
    btn_right = pygame.Rect(SCREEN_WIDTH - 80, SCREEN_HEIGHT - 132, 55, 45)
    btn_action = pygame.Rect(30, SCREEN_HEIGHT - 120, 130, 50)

    questions_bank = [
        {
            "title": "KADİM İSKELETİN BİLMECESİ",
            "question": "Zindandaki iskelet soruyor:\n'Gündüzleri 4 ayak, akşamları 2 ayak, geceleri 3 ayak nedir?'",
            "options": ["1. Kurt", "2. İnsan", "3. Ejderha"],
            "correct": 1
        },
        {
            "title": "BİLGENİN TESTİ",
            "question": "Bilge soruyor:\n'Aydınoğulları Beyliği'nin Ege'deki denizcilik üssü hangisidir?'",
            "options": ["1. Ayasuluğ / Balat", "2. Ankara", "3. Erzurum"],
            "correct": 0
        }
    ]

    def trigger_dialogue(title, text):
        nonlocal mode, dialogue_title, dialogue_text
        mode = "DIALOGUE"
        dialogue_title = title
        dialogue_text = text

    def trigger_question():
        nonlocal mode, active_question, selected_answer
        mode = "QUESTION"
        active_question = random.choice(questions_bank)
        selected_answer = 0

    while running:
        clock.tick(60)
        anim_timer += 1
        
        dx, dy = 0, 0
        touch_action = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if btn_up.collidepoint(pos): dy = -1
                elif btn_down.collidepoint(pos): dy = 1
                elif btn_left.collidepoint(pos): dx = -1
                elif btn_right.collidepoint(pos): dx = 1
                elif btn_action.collidepoint(pos): touch_action = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "MENU"
                if mode == "STORY_INTRO" and (event.key == pygame.K_RETURN or touch_action):
                    mode = "EXPLORE"
                elif mode == "DIALOGUE" and (event.key == pygame.K_RETURN or touch_action):
                    mode = "EXPLORE"
                elif mode in ("VICTORY", "GAMEOVER") and (event.key == pygame.K_RETURN or touch_action):
                    return "MENU"
                elif mode == "QUESTION":
                    if event.key == pygame.K_UP:
                        selected_answer = (selected_answer - 1) % len(active_question["options"])
                    elif event.key == pygame.K_DOWN:
                        selected_answer = (selected_answer + 1) % len(active_question["options"])
                    elif event.key == pygame.K_RETURN or touch_action:
                        if selected_answer == active_question["correct"]:
                            hero["gold"] += 60
                            hero["health"] = min(hero["max_hp"], hero["health"] + 25)
                            trigger_dialogue("DOĞRU CEVAP!", "Bilmeceyi bildin! +60 Altın ve +25 Can kazandın.")
                        else:
                            hero["health"] -= 30
                            if hero["health"] <= 0:
                                mode = "GAMEOVER"
                            else:
                                trigger_dialogue("YANLIŞ CEVAP!", "Yanlış cevap verdin (-30 Can).")

        # Klavye Tuş Kontrolleri ve Anında Hareket
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx = 1
        elif keys[pygame.K_UP] or keys[pygame.K_w]: dy = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]: dy = 1

        # Gecikmeyi (delay) minimuma indirip akıcı hale getirdik
        if mode == "EXPLORE" and (dx != 0 or dy != 0):
            move_delay += 1
            if move_delay > 4:  # Süreyi yarı yarıya düşürdük, anında kayacak
                move_delay = 0
                nx, ny = player_x + dx, player_y + dy
                if 0 <= ny < len(tile_map) and 0 <= nx < len(tile_map[0]):
                    tile = tile_map[ny][nx]
                    if tile != 1:
                        player_x, player_y = nx, ny
                        if tile == 2:
                            hero["gold"] += 50
                            tile_map[ny][nx] = 0
                            trigger_dialogue("HAZİNE SANDIĞI", "Sandığı açtın ve içinde 50 Altın buldun!")
                        elif tile == 4:
                            hero["health"] = min(hero["max_hp"], hero["health"] + 35)
                            tile_map[ny][nx] = 0
                            trigger_dialogue("ŞİFALI İKSİR", "Yeşil iksiri içerek canını tazeledin (+35 Can).")
                        elif tile == 3:
                            hero["health"] -= 20
                            tile_map[ny][nx] = 0
                            if hero["health"] <= 0:
                                mode = "GAMEOVER"
                            else:
                                trigger_dialogue("ZİNDAN İBLİSİ", "Karşına çıkan iblisi devirdin (-20 Can).")
                        elif tile == 6 or tile == 7:
                            tile_map[ny][nx] = 0
                            trigger_question()
                        elif tile == 5:
                            mode = "VICTORY"

        # --- ÇİZİMLER ---
        screen.fill((8, 6, 16))
        
        for y, row in enumerate(tile_map):
            for x, tile in enumerate(row):
                rx = offset_x + x * TILE_SIZE
                ry = offset_y + y * TILE_SIZE
                
                if tile == 1:
                    pygame.draw.rect(screen, (30, 25, 45), (rx, ry, TILE_SIZE, TILE_SIZE), border_radius=4)
                    pygame.draw.rect(screen, (48, 40, 68), (rx + 2, ry + 2, TILE_SIZE - 4, TILE_SIZE - 4), 2, border_radius=4)
                else:
                    pygame.draw.rect(screen, (15, 12, 24), (rx, ry, TILE_SIZE, TILE_SIZE))
                    pygame.draw.rect(screen, (20, 16, 32), (rx, ry, TILE_SIZE, TILE_SIZE), 1)
                    
                    if tile == 2:
                        pygame.draw.rect(screen, (130, 80, 15), (rx + 8, ry + 12, 32, 24), border_radius=4)
                        pygame.draw.rect(screen, NEON_YELLOW, (rx + 8, ry + 18, 32, 4))
                    elif tile == 3:
                        cx, cy = rx + TILE_SIZE // 2, ry + TILE_SIZE // 2
                        pygame.draw.circle(screen, NEON_PINK, (cx, cy + 2), 14)
                        pygame.draw.circle(screen, (255, 30, 30), (cx - 5, ry + 20), 3)
                        pygame.draw.circle(screen, (255, 30, 30), (cx + 5, ry + 20), 3)
                    elif tile == 4:
                        pygame.draw.rect(screen, (0, 240, 120), (rx + 16, ry + 16, 16, 20), border_radius=6)
                    elif tile == 6:
                        rx_c, ry_c = rx + TILE_SIZE//2, ry + TILE_SIZE//2
                        pygame.draw.circle(screen, (200, 200, 210), (rx_c, ry_c), 12)
                        pygame.draw.circle(screen, BLACK, (rx_c - 4, ry_c - 2), 2)
                        pygame.draw.circle(screen, BLACK, (rx_c + 4, ry_c - 2), 2)
                    elif tile == 7:
                        rx_c, ry_c = rx + TILE_SIZE//2, ry + TILE_SIZE//2
                        pygame.draw.circle(screen, (100, 180, 255), (rx_c, ry_c), 12)
                        pygame.draw.rect(screen, WHITE, (rx_c - 8, ry_c + 2, 16, 8), border_radius=2)
                    elif tile == 5:
                        cx, cy = rx + TILE_SIZE // 2, ry + TILE_SIZE // 2
                        pulse = math.sin(anim_timer * 0.12) * 4
                        pygame.draw.polygon(screen, CYAN, [(cx, cy - 20 - pulse), (cx + 16 + pulse, cy), (cx, cy + 20 + pulse), (cx - 16 - pulse, cy)])

        px = offset_x + player_x * TILE_SIZE + TILE_SIZE // 2
        py = offset_y + player_y * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.polygon(screen, NEON_PINK, [(px - 10, py + 4), (px + 10, py + 4), (px, py + 19)])
        pygame.draw.circle(screen, CYAN, (px, py), 13)

        top_bar = pygame.Rect(0, 0, SCREEN_WIDTH, 55)
        pygame.draw.rect(screen, (14, 11, 22), top_bar)
        pygame.draw.line(screen, CYAN, (0, 55), (SCREEN_WIDTH, 55), 2)
        stat_txt = font_hud.render(f"SAVAŞÇI: {hero['name'].upper()}  |  CAN: {hero['health']}  |  ALTIN: {hero['gold']}", True, NEON_YELLOW)
        screen.blit(stat_txt, (20, 18))

        # DOKUNMATİK BUTONLAR (KUTUCUK SORUNU OLMADAN < ve > İŞARETLERİ)
        btn_font = pygame.font.SysFont("Courier", 16, bold=True)
        for rect, label in [(btn_up, "▲"), (btn_down, "▼"), (btn_left, "<"), (btn_right, ">")]:
            pygame.draw.rect(screen, (20, 25, 45), rect, border_radius=8)
            pygame.draw.rect(screen, CYAN, rect, 2, border_radius=8)
            screen.blit(btn_font.render(label, True, WHITE), (rect.centerx - 6, rect.centery - 8))

        pygame.draw.rect(screen, (40, 20, 45), btn_action, border_radius=8)
        pygame.draw.rect(screen, NEON_YELLOW, btn_action, 2, border_radius=8)
        screen.blit(btn_font.render("ONAY / ENTER", True, WHITE), (btn_action.centerx - 50, btn_action.centery - 8))

        if mode == "STORY_INTRO":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 225))
            screen.blit(overlay, (0, 0))
            box = pygame.Rect(50, 70, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 140)
            pygame.draw.rect(screen, (20, 16, 34), box, border_radius=16)
            pygame.draw.rect(screen, CYAN, box, 3, border_radius=16)
            screen.blit(font_title.render(f"ZİNDAN DESTANI: {hero['name'].upper()}", True, NEON_YELLOW), (box.x + 30, box.y + 30))
            screen.blit(font_text.render("Zindandaki bilmeceleri çöz, sandıkları aç ve kristali bul!\n\n[ ENTER VEYA ONAY TUŞUNA BAS ]", True, WHITE), (box.x + 30, box.y + 90))

        elif mode == "QUESTION" and active_question:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            screen.blit(overlay, (0, 0))
            box = pygame.Rect(60, 60, SCREEN_WIDTH - 120, SCREEN_HEIGHT - 120)
            pygame.draw.rect(screen, (22, 18, 38), box, border_radius=16)
            pygame.draw.rect(screen, NEON_YELLOW, box, 3, border_radius=16)
            screen.blit(font_title.render(active_question["title"], True, NEON_YELLOW), (box.x + 30, box.y + 30))
            
            for i, l in enumerate(active_question["question"].split("\n")):
                screen.blit(font_text.render(l, True, WHITE), (box.x + 30, box.y + 80 + i * 26))
                
            for i, opt in enumerate(active_question["options"]):
                o_rect = pygame.Rect(box.x + 30, box.y + 170 + i * 50, box.width - 60, 42)
                color = WHITE if i == selected_answer else (140, 140, 160)
                pygame.draw.rect(screen, (45, 38, 75) if i == selected_answer else (16, 13, 28), o_rect, border_radius=8)
                screen.blit(font_text.render(opt, True, color), (o_rect.x + 20, o_rect.y + 11))

        elif mode == "DIALOGUE":
            box = pygame.Rect(40, SCREEN_HEIGHT - 155, SCREEN_WIDTH - 80, 125)
            pygame.draw.rect(screen, (20, 16, 34), box, border_radius=14)
            pygame.draw.rect(screen, NEON_PINK, box, 2, border_radius=14)
            screen.blit(font_title.render(dialogue_title, True, NEON_YELLOW), (box.x + 20, box.y + 15))
            for i, l in enumerate(dialogue_text.split("\n")):
                screen.blit(font_text.render(l, True, WHITE), (box.x + 20, box.y + 48 + i * 22))

        elif mode in ("VICTORY", "GAMEOVER"):
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 230))
            screen.blit(overlay, (0, 0))
            box = pygame.Rect(SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 - 100, 500, 200)
            pygame.draw.rect(screen, (22, 18, 36), box, border_radius=16)
            pygame.draw.rect(screen, NEON_YELLOW if mode == "VICTORY" else NEON_PINK, box, 3, border_radius=16)
            msg = f"TEBRİKLER {hero['name'].upper()}! KAZANDIN!" if mode == "VICTORY" else "YENİLDİN..."
            screen.blit(font_title.render(msg, True, NEON_YELLOW if mode == "VICTORY" else NEON_PINK), (box.centerx - 130, box.y + 50))
            screen.blit(font_text.render("[ ENTER VEYA ONAY TUŞU ]", True, WHITE), (box.centerx - 90, box.y + 120))

        pygame.display.flip()