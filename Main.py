# Example file showing a circle moving on screen
import pygame
from pygame.math import Vector2

import Renderer
import Items
import Buttons

# Cores usadas pelo jogo. Mantê-las aqui evita depender de um pacote externo
# apenas para obter nomes de cores.
COLOR = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "orange": (255, 165, 0),
    "yellow": (255, 255, 0),
}

SCREEN_SIZE = (1280, 720)
SCREEN_CENTER = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2)
SCREEN_LATERAL_PADDING = int(0.1 * SCREEN_SIZE[0])
SCREEN_VERTICAL_PADDING = int(0.05 * SCREEN_SIZE[1])

def Main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()
    running = True
    dt = 0

    # Inicializa o Renderer
    GameScreen = Renderer.Renderer(screen, COLOR, SCREEN_LATERAL_PADDING, SCREEN_VERTICAL_PADDING)

    # Inicializa os Botões
    menuButtons = Buttons.GameButtons()
    menuButtons.createMenuButtons(SCREEN_SIZE, SCREEN_LATERAL_PADDING, SCREEN_VERTICAL_PADDING)

    player_pos = Vector2(640, 360)

    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Atualiza estado dos botões
        menuButtons.checkButtons(mouse_pos, mouse_click)

        # Movimentação
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_pos.y -= 300 * dt
        if keys[pygame.K_s]:
            player_pos.y += 300 * dt
        if keys[pygame.K_a]:
            player_pos.x -= 300 * dt
        if keys[pygame.K_d]:
            player_pos.x += 300 * dt

        # RENDERIZAÇÃO UNIFICADA
        GameScreen.drawBase()
        GameScreen.drawMenu(menuButtons)  # Desenha os botões usando o Renderer
        GameScreen.drawStatic()
        GameScreen.drawDynamic(player_pos)

        GameScreen.flip()

        dt = clock.tick(60) / 1000

    pygame.quit()


if __name__ == "__main__":
  Main()
