import pygame
from config import WHITE, BLACK, RED, SCREEN_WIDTH, SCREEN_HEIGHT


def show_game_over(screen):
    pygame.font.init()
    clock = pygame.time.Clock()

    # צבעים
    background_color = (240, 240, 240)
    button_color = (200, 50, 50)
    button_hover = (160, 30, 30)
    text_color = BLACK
    title_color = RED

    # פונטים
    title_font = pygame.font.SysFont('Arial', 72, bold=True)
    button_font = pygame.font.SysFont('Arial', 36)

    # טקסטים
    title_text = title_font.render("Game Over", True, title_color)

    restart_text = button_font.render("Restart", True, WHITE)
    exit_text = button_font.render("Exit", True, WHITE)

    # כפתורים (x, y, width, height)
    restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 150, 300, 300, 60)
    exit_button = pygame.Rect(SCREEN_WIDTH // 2 - 150, 400, 300, 60)

    while True:
        mouse_pos = pygame.mouse.get_pos()

        screen.fill(background_color)

        # צייר כותרת
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 120))

        # צייר כפתור Restart
        restart_color = button_hover if restart_button.collidepoint(mouse_pos) else button_color
        pygame.draw.rect(screen, restart_color, restart_button, border_radius=10)
        screen.blit(restart_text, (restart_button.centerx - restart_text.get_width() // 2,
                                   restart_button.centery - restart_text.get_height() // 2))

        # צייר כפתור Exit
        exit_color = button_hover if exit_button.collidepoint(mouse_pos) else button_color
        pygame.draw.rect(screen, exit_color, exit_button, border_radius=10)
        screen.blit(exit_text, (exit_button.centerx - exit_text.get_width() // 2,
                                exit_button.centery - exit_text.get_height() // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'exit'

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if restart_button.collidepoint(event.pos):
                    return 'restart'
                if exit_button.collidepoint(event.pos):
                    return 'exit'

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return 'restart'
                elif event.key == pygame.K_q:
                    return 'exit'

        clock.tick(60)
