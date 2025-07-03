# main.py

import pygame
from config import *
from ui.menu import show_menu
from logic.game_controller import GameController
from ui.game_over import show_game_over

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tank Destroyer")
clock = pygame.time.Clock()

def main():
    while True:
        choice = show_menu(screen)
        if choice == 'start':
            controller = GameController(screen)
            controller.run()
        elif choice == 'exit':
            break
        else:
            continue

        show_game_over(screen)

    pygame.quit()

if __name__ == "__main__":
    main()
