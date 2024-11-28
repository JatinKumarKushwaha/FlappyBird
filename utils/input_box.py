import pygame


class InputBox(pygame.sprite.Sprite):
    def __init__(
        self, x, y, width, height, font=None, text="", placeRect="center"
    ) -> None:
        super().__init__()

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fillColors = {
            "normal": "#ffffff",
            "hover": "#666666",
            "active": "#333333",
        }

        self.placeRect = placeRect

        if font == None:
            font = pygame.font.SysFont("comicsans", 60)
        else:
            self.font = font

        self.text = text
        self.active = False
        self.draw()

    def draw(self):
        textBoxFontSurface = self.font.render(self.text, True, (20, 20, 20))
        self.image = pygame.Surface(
            (
                max(self.width, textBoxFontSurface.get_width() + 10),
                textBoxFontSurface.get_height() + 10,
            ),
            pygame.SRCALPHA,
        )
        if self.fillColors["normal"]:
            self.image.fill(self.fillColors["normal"])
        self.image.blit(textBoxFontSurface, (5, 5))
        pygame.draw.rect(
            self.image,
            self.fillColors["normal"],
            self.image.get_rect().inflate(-2, -2),
            2,
        )
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and not self.active:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            self.draw()

    def getText(self):
        return self.text

    def betterHandler(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_BACKSPACE]:
            self.text = self.text[:-1]
        else:
            pygame.key.start_text_input()
            pygame.key.stop_text_input()

    def update(self, event):
        self.handle_event(event)
