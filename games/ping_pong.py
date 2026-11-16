import pygame
import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, CYAN, NEON_PINK, NEON_YELLOW

def run_game(screen, clock):
    running = True
    
    player = pygame.Rect(40, SCREEN_HEIGHT // 2 - 40, 15, 80)
    opponent = pygame.Rect(SCREEN_WIDTH - 55, SCREEN_HEIGHT // 2 - 40, 15, 80)
    ball = pygame.Rect(SCREEN_WIDTH // 2 - 10, SCREEN_HEIGHT // 2 - 10, 20, 20)
    
    ball_speed_x = 5 * random.choice((1, -1))
    ball_speed_y = 5 * random.choice((1, -1))
    
    player_score = 0
    opponent_score = 0
    
    font = pygame.font.SysFont("Courier", 18, bold=True)
    
    # --- DOKUNMATİK BUTONLAR (PING PONG) ---
    btn_up = pygame.Rect(20, SCREEN_HEIGHT - 120, 65, 50)
    btn_down = pygame.Rect(20, SCREEN_HEIGHT - 65, 65, 50)
    
    moving_up = False
    moving_down = False

    while running:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if btn_up.collidepoint(pos):
                    moving_up = True
                elif btn_down.collidepoint(pos):
                    moving_down = True
                    
            if event.type == pygame.MOUSEBUTTONUP:
                moving_up = False
                moving_down = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "MENU"

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_UP] or keys[pygame.K_w] or moving_up) and player.top > 60:
            player.y -= 7
        if (keys[pygame.K_DOWN] or keys[pygame.K_s] or moving_down) and player.bottom < SCREEN_HEIGHT - 10:
            player.y += 7

        if opponent.centery < ball.centery and opponent.bottom < SCREEN_HEIGHT - 10:
            opponent.y += 5
        elif opponent.centery > ball.centery and opponent.top > 60:
            opponent.y -= 5

        ball.x += ball_speed_x
        ball.y += ball_speed_y

        if ball.top <= 60 or ball.bottom >= SCREEN_HEIGHT:
            ball_speed_y *= -1

        if ball.colliderect(player) or ball.colliderect(opponent):
            ball_speed_x *= -1.1
            
        if ball.left <= 0:
            opponent_score += 1
            ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            ball_speed_x = 5 * random.choice((1, -1))
        elif ball.right >= SCREEN_WIDTH:
            player_score += 1
            ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            ball_speed_x = 5 * random.choice((1, -1))

        # --- ÇİZİM ---
        screen.fill((10, 8, 20))
        
        top_bar = pygame.Rect(0, 0, SCREEN_WIDTH, 55)
        pygame.draw.rect(screen, (15, 12, 25), top_bar)
        pygame.draw.line(screen, CYAN, (0, 55), (SCREEN_WIDTH, 55), 2)
        
        score_txt = font.render(f"OYUNCU: {player_score}   |   RAKİP: {opponent_score}   |   [ESC] MENÜ", True, NEON_YELLOW)
        screen.blit(score_txt, (30, 18))
        
        pygame.draw.aaline(screen, (50, 50, 80), (SCREEN_WIDTH // 2, 60), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))
        
        pygame.draw.rect(screen, CYAN, player, border_radius=4)
        pygame.draw.rect(screen, NEON_PINK, opponent, border_radius=4)
        pygame.draw.ellipse(screen, WHITE, ball)

        # Dokunmatik Butonlar
        btn_font = pygame.font.SysFont("Courier", 16, bold=True)
        
        pygame.draw.rect(screen, (20, 25, 45), btn_up, border_radius=8)
        pygame.draw.rect(screen, CYAN, btn_up, 2, border_radius=8)
        screen.blit(btn_font.render("▲ YUKARI", True, WHITE), (btn_up.centerx - 32, btn_up.centery - 10))
        
        pygame.draw.rect(screen, (20, 25, 45), btn_down, border_radius=8)
        pygame.draw.rect(screen, CYAN, btn_down, 2, border_radius=8)
        screen.blit(btn_font.render("▼ AŞAĞI", True, WHITE), (btn_down.centerx - 30, btn_down.centery - 10))

        pygame.display.flip()