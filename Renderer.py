import pygame
import Buttons

class Renderer:
    def __init__(
            self,
            screen,
            colorDict,
            SCREEN_LATERAL_PADDING,
            SCREEN_VERTICAL_PADDING,
            defaultFontPath: str = "DeterminationMono.ttf",
            fontSize: int = 28,
    ):
        self.screen = screen
        self.COLOR = colorDict
        self.SCREEN_LATERAL_PADDING = SCREEN_LATERAL_PADDING
        self.SCREEN_VERTICAL_PADDING = SCREEN_VERTICAL_PADDING
        self.fontSize = fontSize

        # Cache de fontes para performance
        self.loaded_fonts = {}

        # Carrega a fonte padrão do Undertale
        try:
            self.defaultFont = pygame.font.Font(defaultFontPath, fontSize)
            self.loaded_fonts[defaultFontPath] = self.defaultFont
        except FileNotFoundError:
            print(
                f"Aviso: Fonte '{defaultFontPath}' não encontrada. Usando a fonte"
                " do sistema."
            )
            self.defaultFont = pygame.font.SysFont("Courier", fontSize)

    def getFont(self, fontPath: str) -> pygame.font.Font:
        """Retorna a fonte solicitada (carrega e salva em cache se ainda não existir)."""
        if not fontPath:
            return self.defaultFont

        if fontPath not in self.loaded_fonts:
            try:
                self.loaded_fonts[fontPath] = pygame.font.Font(fontPath, self.fontSize)
            except FileNotFoundError:
                print(
                    f"Aviso: Fonte customizada '{fontPath}' não encontrada. Usando a"
                    " padrão."
                )
                return self.defaultFont

        return self.loaded_fonts[fontPath]

    def drawBase(self):
        self.screen.fill(self.COLOR["black"])

    def drawButton(self, button: Buttons.Button):
        """Desenha um único botão recebido."""
        # 1. Seleciona a fonte correta (se button.buttonFont for None, retorna self.defaultFont)
        font = self.getFont(button.buttonFont)

        # Define a cor de borda dependendo do estado do botão (hover, click ou normal)
        borderColor = button.colorBorder
        if button.clicked:
            borderColor = button.colorClick
        elif button.hovered:
            borderColor = button.colorHover

        # 2. Renderiza o texto
        text_surface = font.render(
            button.buttonName, True, self.COLOR[borderColor]
        )
        text_rect = text_surface.get_rect(center=button.position)

        # 3. Desenha a caixa (borda/fundo estilo Undertale)
        padding = 14
        box_rect = text_rect.inflate(padding * 3, padding * 2)

        pygame.draw.rect(self.screen, self.COLOR[button.colorFill], box_rect)
        pygame.draw.rect(
            self.screen, self.COLOR[borderColor], box_rect, 3
        )  # Borda de 3px

        # 4. Desenha o texto por cima
        self.screen.blit(text_surface, text_rect)

    def drawMenu(self, gameButtons: Buttons.GameButtons):
        """Desenha a lista completa de botões do menu."""
        for button in gameButtons.listButtons:
            self.drawButton(button)

    def drawStatic(self):
        pass


    def drawDynamic(self, player_pos):
        pygame.draw.circle(self.screen, self.COLOR["white"], player_pos, 40)


    def flip(self):
        pygame.display.flip()