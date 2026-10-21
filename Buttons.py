from pygame.math import Vector2
import pygame as pg

class GameButtons:
    def __init__(self, listButtons=None):
        if listButtons is None:
            listButtons = []
        self.listButtons = listButtons

    def addButton(self, button):
        self.listButtons.append(button)

    def removeButton(self, button):
        self.listButtons.remove(button)

    def createMenuButtons(self, SCREEN_SIZE, SCREEN_LATERAL_PADDING, SCREEN_VERTICAL_PADDING):
        # Exemplo de criação de botões no padrão Undertale (sem passar fonte -> usa a padrão)
        buttonFight = Button(
            buttonName="FIGHT",
            position=Vector2(SCREEN_LATERAL_PADDING + SCREEN_SIZE[0] * 0.1, SCREEN_SIZE[1] * 0.9 - SCREEN_VERTICAL_PADDING),
            colorBorder="orange",
            colorFill="black",
            colorHover="yellow",
            colorClick="white",
            action="FIGHT",
        )
        buttonAct = Button(
            buttonName="ACT",
            position=Vector2(SCREEN_LATERAL_PADDING + SCREEN_SIZE[0] * 0.35, SCREEN_SIZE[1] * 0.9 - SCREEN_VERTICAL_PADDING),
            colorBorder="orange",
            colorFill="black",
            colorHover="yellow",
            colorClick="white",
            action="ACT",
        )

        buttonItem = Button(
            buttonName="ITEM",
            position=Vector2(SCREEN_LATERAL_PADDING + SCREEN_SIZE[0] * 0.5, SCREEN_SIZE[1] * 0.9 - SCREEN_VERTICAL_PADDING),
            colorBorder="orange",
            colorFill="black",
            colorHover="yellow",
            colorClick="white",
            action="ITEM",
        )

        buttonMercy = Button(
            buttonName="MERCY",
            position=Vector2(SCREEN_LATERAL_PADDING + SCREEN_SIZE[0] * 0.75, SCREEN_SIZE[1] * 0.9 - SCREEN_VERTICAL_PADDING),
            colorBorder="orange",
            colorFill="black",
            colorHover="yellow",
            colorClick="white",
            action="MERCY",
        )
        self.addButton(buttonFight)
        self.addButton(buttonAct)
        self.addButton(buttonItem)
        self.addButton(buttonMercy)


    def checkButtons(self, mouse_pos, mouse_click):
        """Atualiza o estado de hover e clique dos botões baseando-se no mouse."""
        for button in self.listButtons:
            # Cria um rect aproximado para testar colisão com o mouse
            # (Você pode ajustar a largura/altura se quiser)
            rect = pg.Rect(
                button.position.x - 50, button.position.y - 20, 100, 40
            )


            button.hovered = rect.collidepoint(mouse_pos)
            if button.hovered and mouse_click[0]:
                button.clicked = True
            else:
                button.clicked = False




class Button:
    def __init__(
            self,
            buttonName: str,
            position: Vector2,
            colorBorder: str,
            colorFill: str,
            colorHover: str,
            colorClick: str,
            action: str,
            buttonFont: str = None,  # Opcional: Se None, o Renderer usa a fonte padrão
    ):
        self.buttonName = buttonName
        self.buttonFont = buttonFont  # Pode ser o caminho de um .ttf customizado ou None
        self.position = position
        self.colorBorder = colorBorder
        self.colorFill = colorFill
        self.colorHover = colorHover
        self.colorClick = colorClick
        self.clicked = False
        self.hovered = False
        self.action = action
