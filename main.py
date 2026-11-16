import pygame
import sys
import json
import os
import importlib
import pkgutil
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, DARK_BLUE, CYAN, NEON_PINK, NEON_YELLOW, WHITE, GRAY, DARK_GRAY
import games

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("RETRO CORE OS - Mobile Ready v3.2")
clock = pygame.time.Clock()

PROFILES_FILE = "profiles.json"

def load_profiles():
    if os.path.exists(PROFILES_FILE):
        with open(PROFILES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if "Oyuncular" in data and len(data["Oyuncular"]) > 0:
                return data
    return {"Oyuncular": ["Oyuncu1"], "Aktif": "Oyuncu1"}

def save_profiles(data):
    with open(PROFILES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

profiles_data = load_profiles()
current_user = profiles_data.get("Aktif", "Oyuncu1")

if current_user not in profiles_data["Oyuncular"] and len(profiles_data["Oyuncular"]) > 0:
    current_user = profiles_data["Oyuncular"][0]
    profiles_data["Aktif"] = current_user

def load_dynamic_games():
    """games/ klasöründeki tüm Python oyun dosyalarını otomatik tarar ve yükler"""
    discovered_games = []
    games_path = games.__path__
    
    for _, modname, _ in pkgutil.iter_modules(games_path):
        if modname == "__init__":
            continue
        try:
            module = importlib.import_module(f"games.{modname}")
            if hasattr(module, "run_game"):
                clean_name = modname.replace("_", " ").upper()
                discovered_games.append({
                    "name": clean_name,
                    "module": module,
                    "id": modname
                })
        except Exception as e:
            print(f"Oyun yüklenirken hata oluştu ({modname}): {e}")
            
    return discovered_games

games_list = load_dynamic_games()
selected_index = 0

# --- DOKUNMATİK KONTROL BUTONLARI (KUTUCUK SORUNU GİDERİLDİ) ---
btn_up = pygame.Rect(SCREEN_WIDTH - 140, SCREEN_HEIGHT - 170, 55, 45)
btn_down = pygame.Rect(SCREEN_WIDTH - 140, SCREEN_HEIGHT - 110, 55, 45)
btn_left = pygame.Rect(SCREEN_WIDTH - 200, SCREEN_HEIGHT - 140, 55, 45)
btn_right = pygame.Rect(SCREEN_WIDTH - 80, SCREEN_HEIGHT - 140, 55, 45)
btn_enter = pygame.Rect(30, SCREEN_HEIGHT - 120, 120, 50)
btn_profile = pygame.Rect(160, SCREEN_HEIGHT - 120, 120, 50)

def user_creation_screen():
    input_text = ""
    font = pygame.font.SysFont("Courier", 24, bold=True)
    title_font = pygame.font.SysFont("Courier", 30, bold=True)
    
    building = True
    while building:
        clock.tick(FPS)
        screen.fill(BLACK)
        
        panel_rect = pygame.Rect(SCREEN_WIDTH // 2 - 220, 160, 440, 260)
        pygame.draw.rect(screen, DARK_BLUE, panel_rect, border_radius=16)
        pygame.draw.rect(screen, CYAN, panel_rect, 2, border_radius=16)
        
        txt = title_font.render("YENİ KULLANICI EKLE", True, NEON_PINK)
        screen.blit(txt, (SCREEN_WIDTH // 2 - txt.get_width() // 2, 190))
        
        input_rect = pygame.Rect(SCREEN_WIDTH // 2 - 170, 260, 340, 50)
        pygame.draw.rect(screen, DARK_GRAY, input_rect, border_radius=10)
        pygame.draw.rect(screen, NEON_YELLOW, input_rect, 2, border_radius=10)
        
        txt_surface = font.render(input_text + "_", True, WHITE)
        screen.blit(txt_surface, (input_rect.x + 15, input_rect.y + 14))
        
        info = font.render("ENTER: Kaydet | ESC: İptal", True, GRAY)
        screen.blit(info, (SCREEN_WIDTH // 2 - info.get_width() // 2, 350))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and input_text.strip():
                    new_name = input_text.strip()
                    if new_name not in profiles_data["Oyuncular"]:
                        profiles_data["Oyuncular"].append(new_name)
                    profiles_data["Aktif"] = new_name
                    save_profiles(profiles_data)
                    return new_name
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_ESCAPE:
                    return None
                else:
                    if len(input_text) < 12 and event.unicode.isprintable():
                        input_text += event.unicode

def profile_management_screen():
    global current_user
    font = pygame.font.SysFont("Courier", 20, bold=True)
    title_font = pygame.font.SysFont("Courier", 26, bold=True)
    idx = 0
    
    managing = True
    while managing:
        clock.tick(FPS)
        screen.fill(BLACK)
        
        panel_rect = pygame.Rect(SCREEN_WIDTH // 2 - 260, 90, 520, 440)
        pygame.draw.rect(screen, DARK_BLUE, panel_rect, border_radius=16)
        pygame.draw.rect(screen, NEON_PINK, panel_rect, 2, border_radius=16)
        
        title = title_font.render("PROFİL YÖNETİM MERKEZİ", True, CYAN)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 115))
        
        players = profiles_data["Oyuncular"] + ["+ YENİ KULLANICI EKLE"]
        
        for i, p_name in enumerate(players):
            y = 180 + i * 50
            rect = pygame.Rect(SCREEN_WIDTH // 2 - 210, y, 420, 40)
            
            if i == idx:
                pygame.draw.rect(screen, DARK_GRAY, rect, border_radius=8)
                pygame.draw.rect(screen, NEON_YELLOW, rect, 2, border_radius=8)
                color = WHITE
                prefix = "> "
            else:
                pygame.draw.rect(screen, (20, 25, 40), rect, border_radius=8)
                color = GRAY
                prefix = "  "
                
            txt = font.render(f"{prefix}{p_name}", True, color)
            screen.blit(txt, (SCREEN_WIDTH // 2 - 190, y + 10))
            
        info = font.render("Yön Tuşları: Seç | ENTER: Aktif Yap | DEL: Sil | ESC: Geri", True, WHITE)
        screen.blit(info, (SCREEN_WIDTH // 2 - info.get_width() // 2, SCREEN_HEIGHT - 90))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                total_items = len(players)
                if event.key == pygame.K_UP:
                    idx = (idx - 1) % total_items
                elif event.key == pygame.K_DOWN:
                    idx = (idx + 1) % total_items
                elif event.key == pygame.K_RETURN:
                    total_players = len(profiles_data["Oyuncular"])
                    if idx < total_players:
                        current_user = profiles_data["Oyuncular"][idx]
                        profiles_data["Aktif"] = current_user
                        save_profiles(profiles_data)
                        managing = False
                    else:
                        res = user_creation_screen()
                        if res:
                            current_user = res
                            managing = False
                elif event.key in (pygame.K_DELETE, pygame.K_BACKSPACE):
                    total_players = len(profiles_data["Oyuncular"])
                    if idx < total_players and total_players > 1:
                        removed_user = profiles_data["Oyuncular"].pop(idx)
                        if current_user == removed_user:
                            current_user = profiles_data["Oyuncular"][0]
                        profiles_data["Aktif"] = current_user
                        save_profiles(profiles_data)
                        idx = 0
                elif event.key == pygame.K_ESCAPE:
                    managing = False

def draw_menu():
    screen.fill(BLACK)
    
    top_bar = pygame.Rect(0, 0, SCREEN_WIDTH, 55)
    pygame.draw.rect(screen, DARK_BLUE, top_bar)
    pygame.draw.line(screen, CYAN, (0, 55), (SCREEN_WIDTH, 55), 2)
    
    user_font = pygame.font.SysFont("Courier", 18, bold=True)
    user_txt = user_font.render(f"OYUNCU: {current_user}", True, NEON_YELLOW)
    screen.blit(user_txt, (30, 18))
    
    hint_txt = user_font.render("[P] PROFİL", True, CYAN)
    screen.blit(hint_txt, (SCREEN_WIDTH - hint_txt.get_width() - 30, 18))
    
    title_font = pygame.font.SysFont("Courier", 38, bold=True)
    title_surface = title_font.render("RETRO CORE OS", True, NEON_PINK)
    screen.blit(title_surface, (SCREEN_WIDTH // 2 - title_surface.get_width() // 2, 75))
    
    sub_title = user_font.render(f"YÜKLÜ OYUN SAYISI: {len(games_list)}", True, GRAY)
    screen.blit(sub_title, (SCREEN_WIDTH // 2 - sub_title.get_width() // 2, 125))
    
    item_font = pygame.font.SysFont("Courier", 18, bold=True)
    
    if len(games_list) == 0:
        no_game = item_font.render("HİÇ OYUN BULUNAMADI (games/ KONTROL ET)", True, NEON_PINK)
        screen.blit(no_game, (SCREEN_WIDTH // 2 - no_game.get_width() // 2, 230))
    else:
        for index, game in enumerate(games_list):
            y_pos = 170 + index * 65
            rect = pygame.Rect(SCREEN_WIDTH // 2 - 260, y_pos, 520, 55)
            
            if index == selected_index:
                pygame.draw.rect(screen, DARK_BLUE, rect, border_radius=12)
                pygame.draw.rect(screen, CYAN, rect, 3, border_radius=12)
                color = WHITE
                pygame.draw.polygon(screen, NEON_YELLOW, [
                    (SCREEN_WIDTH // 2 - 240, y_pos + 18),
                    (SCREEN_WIDTH // 2 - 228, y_pos + 27),
                    (SCREEN_WIDTH // 2 - 240, y_pos + 36)
                ])
            else:
                pygame.draw.rect(screen, DARK_GRAY, rect, border_radius=12)
                pygame.draw.rect(screen, GRAY, rect, 1, border_radius=12)
                color = GRAY
                
            txt_surface = item_font.render(game["name"], True, color)
            screen.blit(txt_surface, (SCREEN_WIDTH // 2 - txt_surface.get_width() // 2, y_pos + 16))
        
    # --- EKRAN ÜSTÜ DOKUNMATİK BUTONLAR (SORUNSUZ OKLAR) ---
    btn_font = pygame.font.SysFont("Courier", 16, bold=True)
    
    for rect, label in [(btn_up, "▲"), (btn_down, "▼"), (btn_left, "<"), (btn_right, ">")]:
        pygame.draw.rect(screen, DARK_BLUE, rect, border_radius=8)
        pygame.draw.rect(screen, CYAN, rect, 2, border_radius=8)
        lbl = btn_font.render(label, True, WHITE)
        screen.blit(lbl, (rect.centerx - lbl.get_width()//2, rect.centery - lbl.get_height()//2))
        
    for rect, label in [(btn_enter, "SEÇ / ENTER"), (btn_profile, "PROFİL")]:
        pygame.draw.rect(screen, (30, 20, 45), rect, border_radius=8)
        pygame.draw.rect(screen, NEON_YELLOW, rect, 2, border_radius=8)
        lbl = btn_font.render(label, True, WHITE)
        screen.blit(lbl, (rect.centerx - lbl.get_width()//2, rect.centery - lbl.get_height()//2))

    pygame.display.flip()

def main():
    global selected_index, current_user
    running = True
    
    while running:
        clock.tick(FPS)
        draw_menu()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if btn_up.collidepoint(pos) and len(games_list) > 0:
                    selected_index = (selected_index - 1) % len(games_list)
                elif btn_down.collidepoint(pos) and len(games_list) > 0:
                    selected_index = (selected_index + 1) % len(games_list)
                elif btn_enter.collidepoint(pos) and len(games_list) > 0:
                    chosen_game = games_list[selected_index]
                    if chosen_game["module"] is not None:
                        if "DUNGEON" in chosen_game["id"].upper():
                            chosen_game["module"].run_game(screen, clock, username=current_user)
                        else:
                            chosen_game["module"].run_game(screen, clock)
                elif btn_profile.collidepoint(pos):
                    profile_management_screen()

            if event.type == pygame.KEYDOWN:
                if len(games_list) > 0:
                    if event.key == pygame.K_UP:
                        selected_index = (selected_index - 1) % len(games_list)
                    elif event.key == pygame.K_DOWN:
                        selected_index = (selected_index + 1) % len(games_list)
                
                if event.key == pygame.K_p:
                    profile_management_screen()
                elif event.key == pygame.K_RETURN and len(games_list) > 0:
                    chosen_game = games_list[selected_index]
                    if chosen_game["module"] is not None:
                        if "DUNGEON" in chosen_game["id"].upper():
                            result = chosen_game["module"].run_game(screen, clock, username=current_user)
                        else:
                            result = chosen_game["module"].run_game(screen, clock)
                            
                        if result == "QUIT":
                            running = False
                elif event.key == pygame.K_ESCAPE:
                    running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()