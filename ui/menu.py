import pygame
from config import WHITE, BLACK, RED, BLUE, SCREEN_WIDTH, SCREEN_HEIGHT


def show_menu(screen):
    pygame.font.init()
    clock = pygame.time.Clock()

    # צבעים
    background_color = (220, 220, 220)
    button_color = (50, 150, 255)
    button_hover = (30, 120, 220)
    text_color = BLACK
    title_color = (10, 10, 80)

    # פונטים
    title_font = pygame.font.SysFont('Arial', 72, bold=True)
    button_font = pygame.font.SysFont('Arial', 36)

    # טקסטים
    title_text = title_font.render("Tank Destroyer", True, title_color)
    start_text = button_font.render("Start Game", True, WHITE)
    exit_text = button_font.render("Exit", True, WHITE)

    # כפתורים (x, y, width, height)
    start_button = pygame.Rect(SCREEN_WIDTH // 2 - 150, 300, 300, 60)
    exit_button = pygame.Rect(SCREEN_WIDTH // 2 - 150, 400, 300, 60)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        screen.fill(background_color)

        # צייר כותרת
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 120))

        # צייר כפתור Start
        start_color = button_hover if start_button.collidepoint(mouse_pos) else button_color
        pygame.draw.rect(screen, start_color, start_button, border_radius=10)
        screen.blit(start_text, (start_button.centerx - start_text.get_width() // 2,
                                 start_button.centery - start_text.get_height() // 2))

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
                if start_button.collidepoint(event.pos):
                    return 'start'
                if exit_button.collidepoint(event.pos):
                    return 'exit'

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    return 'start'
                elif event.key == pygame.K_q:
                    return 'exit'

        clock.tick(60)
