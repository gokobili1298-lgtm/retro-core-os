import pygame
import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, CYAN, NEON_PINK, NEON_YELLOW

def run_game(screen, clock):
    running = True
    
    player = pygame.Rect(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT - 80, 50, 30)
    player_speed = 6
    
    bullets = []
    enemies = []
    score = 0
    health = 100
    spawn_timer = 0
    
    font = pygame.font.SysFont("Courier", 18, bold=True)
    title_font = pygame.font.SysFont("Courier", 28, bold=True)
    
   # --- DOKUNMATİK BUTONLAR (DÜZGÜN YERLEŞİM VE OKLAR) ---
    btn_left = pygame.Rect(20, SCREEN_HEIGHT - 100, 70, 55)
    btn_right = pygame.Rect(100, SCREEN_HEIGHT - 100, 70, 55)
    btn_fire = pygame.Rect(SCREEN_WIDTH - 110, SCREEN_HEIGHT - 100, 90, 55)
    
    moving_left = False
    moving_right = False

    while running:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if btn_left.collidepoint(pos):
                    moving_left = True
                elif btn_right.collidepoint(pos):
                    moving_right = True
                elif btn_fire.collidepoint(pos):
                    bullets.append(pygame.Rect(player.centerx - 3, player.top - 10, 6, 12))
            
            if event.type == pygame.MOUSEBUTTONUP:
                moving_left = False
                moving_right = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "MENU"
                if event.key == pygame.K_SPACE:
                    bullets.append(pygame.Rect(player.centerx - 3, player.top - 10, 6, 12))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a] or moving_left:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d] or moving_right:
            player.x += player_speed
            
        player.x = max(20, min(SCREEN_WIDTH - player.width - 20, player.x))

        for bullet in bullets[:]:
            bullet.y -= 10
            if bullet.bottom < 0:
                bullets.remove(bullet)

        spawn_timer += 1
        if spawn_timer > 30:
            spawn_timer = 0
            ex = random.randint(50, SCREEN_WIDTH - 90)
            enemies.append(pygame.Rect(ex, -40, 42, 42))

        for enemy in enemies[:]:
            enemy.y += 4
            
            if player.colliderect(enemy):
                enemies.remove(enemy)
                health -= 20
                if health <= 0:
                    health = 0

            for bullet in bullets[:]:
                if bullet.colliderect(enemy):
                    if bullet in bullets: bullets.remove(bullet)
                    if enemy in enemies: enemies.remove(enemy)
                    score += 10
                    break

            if enemy.top > SCREEN_HEIGHT:
                enemies.remove(enemy)
                health -= 10
                if health <= 0:
                    health = 0

        # --- ÇİZİMLER ---
        screen.fill((10, 8, 20))
        
        # Oyuncu Gemisi
        pygame.draw.polygon(screen, CYAN, [
            (player.centerx, player.top),
            (player.left, player.bottom),
            (player.right, player.bottom)
        ])
        pygame.draw.rect(screen, NEON_YELLOW, (player.centerx - 2, player.top + 6, 4, 10))
        
        # Mermiler
        for bullet in bullets:
            pygame.draw.rect(screen, NEON_YELLOW, bullet, border_radius=3)

        # Düşmanlar (Orijinal Detaylı Tasarım)
        for enemy in enemies:
            pygame.draw.rect(screen, NEON_PINK, enemy, border_radius=8)
            pygame.draw.circle(screen, WHITE, (enemy.centerx, enemy.centery), 6)
            pygame.draw.circle(screen, BLACK, (enemy.centerx, enemy.centery), 2)

        # Üst Bilgi Çubuğu (HUD)
        top_bar = pygame.Rect(0, 0, SCREEN_WIDTH, 55)
        pygame.draw.rect(screen, (15, 12, 25), top_bar)
        pygame.draw.line(screen, CYAN, (0, 55), (SCREEN_WIDTH, 55), 2)
        hud_txt = font.render(f"SKOR: {score}  |  CAN: {health}%  |  [ESC] MENÜ", True, NEON_YELLOW)
        screen.blit(hud_txt, (25, 18))

       # DOKUNMATİK BUTONLAR ÇİZİMİ
        btn_font = pygame.font.SysFont("Courier", 16, bold=True)
        pygame.draw.rect(screen, (20, 25, 45), btn_left, border_radius=10)
        pygame.draw.rect(screen, CYAN, btn_left, 2, border_radius=10)
        screen.blit(btn_font.render("< SOL", True, WHITE), (btn_left.centerx - 20, btn_left.centery - 10))
        
        pygame.draw.rect(screen, (20, 25, 45), btn_right, border_radius=10)
        pygame.draw.rect(screen, CYAN, btn_right, 2, border_radius=10)
        screen.blit(font.render("SAG >", True, WHITE), (btn_right.centerx - 20, btn_right.centery - 10))
        
        pygame.draw.rect(screen, (45, 20, 35), btn_fire, border_radius=10)
        pygame.draw.rect(screen, NEON_PINK, btn_fire, 2, border_radius=10)
        screen.blit(font.render("ATES", True, WHITE), (btn_fire.centerx - 18, btn_fire.centery - 10))
        if health <= 0:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 220))
            screen.blit(overlay, (0, 0))
            box = pygame.Rect(SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 - 80, 400, 160)
            pygame.draw.rect(screen, (22, 18, 36), box, border_radius=14)
            pygame.draw.rect(screen, NEON_PINK, box, 3, border_radius=14)
            screen.blit(title_font.render("OYUN BİTTİ", True, NEON_PINK), (box.centerx - 75, box.y + 35))
            screen.blit(font.render("[ ENTER VEYA ESC: Menü ]", True, WHITE), (box.centerx - 100, box.y + 105))
            pygame.display.flip()
            
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                        return "MENU"
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        return "MENU"

        pygame.display.flip()