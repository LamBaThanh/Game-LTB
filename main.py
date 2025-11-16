from menu import show_menu
from game import run_game
import pygame, sys

def main():
    pygame.init()
    while True:
        rows, cols = show_menu()
        run_game(rows, cols)

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pygame.quit()
        sys.exit()

#python -m PyInstaller --onefile --windowed --add-data "assets;assets" main.py