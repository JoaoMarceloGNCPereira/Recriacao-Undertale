"""Verifica se os módulos principais inicializam e conseguem desenhar um frame."""
import os
import sys
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pygame
import Buttons
import Main
import Renderer


def main():
    pygame.init()
    try:
        screen = pygame.display.set_mode(Main.SCREEN_SIZE)
        renderer = Renderer.Renderer(screen, Main.COLOR, 10, 10)
        buttons = Buttons.GameButtons()
        buttons.createMenuButtons(Main.SCREEN_SIZE, 10, 10)
        renderer.drawBase()
        renderer.drawMenu(buttons)
        renderer.drawDynamic((100, 100))
        pygame.display.flip()
    finally:
        pygame.quit()

    print("Smoke test passed")


if __name__ == "__main__":
    main()
