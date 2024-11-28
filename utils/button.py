import pygame


class Button:
    def __init__(
        self, x, y, width, height, buttonText="Button", font=None, placeRect="center"
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fillColors = {
            "normal": "#ffffff",
            "hover": "#666666",
            "pressed": "#333333",
        }

        if font == None:
            self.font = pygame.font.SysFont("comicsans", 60)
        else:
            self.font = font

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Placement of the buttonRect
        # Possilbe values
        # ["top", "left", "bottom", "right", "topleft", "bottomleft", "topright", "bottomright", "midtop", "midleft", "midbottom", "midright", "center", "centerx", "centery"]:
        if placeRect == "top":
            self.buttonRect.top = 0
        elif placeRect == "left":
            self.buttonRect.left = 0
        elif placeRect == "bottom":
            self.buttonRect.bottom = 0
        elif placeRect == "right":
            self.buttonRect.right = 0
        elif placeRect == "topleft":
            self.buttonRect.topleft = (x, y)
        elif placeRect == "bottomleft":
            self.buttonRect.bottomleft = (x, y)
        elif placeRect == "topright":
            self.buttonRect.topright = (x, y)
        elif placeRect == "bottomright":
            self.buttonRect.bottomright = (x, y)
        elif placeRect == "midtop":
            self.buttonRect.midtop = (x, y)
        elif placeRect == "midleft":
            self.buttonRect.midleft = (x, y)
        elif placeRect == "midbottom":
            self.buttonRect.midbottom = (x, y)
        elif placeRect == "midright":
            self.buttonRect.midright = (x, y)
        elif placeRect == "center":
            self.buttonRect.center = (self.x, self.y)
        elif placeRect == "centerx":
            self.buttonRect.centerx = 0
        elif placeRect == "centery":
            self.buttonRect.centery = 0
        else:
            self.buttonRect.center = (x, y)

        self.buttonFontSurface = self.font.render(buttonText, True, (20, 20, 20))

    def draw(self, screen):
        self.buttonSurface.blit(
            self.buttonFontSurface,
            [
                self.buttonRect.width / 2 - self.buttonFontSurface.get_rect().width / 2,
                self.buttonRect.height / 2
                - self.buttonFontSurface.get_rect().height / 2,
            ],
        )
        screen.blit(self.buttonSurface, self.buttonRect)

    def animate(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors["normal"])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors["hover"])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors["pressed"])

    def isPressed(self):
        mousePos = pygame.mouse.get_pos()
        if (
            self.buttonRect.collidepoint(mousePos)
            and pygame.mouse.get_pressed(num_buttons=3)[0]
        ):
            return True
        return False

    def update(self, screen):
        self.draw(screen)
        self.animate()
