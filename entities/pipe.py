import pygame
from random import randrange


class Pipe(pygame.sprite.Sprite):
    def __init__(self, resolution, type, pipe_x_pos):
        super().__init__()

        # Screen resolution format: tuple(width, height)
        self.resolution = resolution

        # Normal pipe
        self.pipe = pygame.image.load("assets/graphics/pipe.png").convert_alpha()
        self.pipe = pygame.transform.rotozoom(self.pipe, 0, 1.0)

        # Upsidedown pipe
        self.opposite_pipe = pygame.image.load(
            "assets/graphics/pipe.png"
        ).convert_alpha()
        # self.opposite_pipe = pygame.transform.flip(self.opposite_pipe, True, False)
        self.opposite_pipe = pygame.transform.rotozoom(self.opposite_pipe, 180, 1.0)

        if type:
            self.image = self.pipe
            self.rect = self.image.get_rect(midbottom=(pipe_x_pos, self.resolution[1]))
        else:
            self.image = self.opposite_pipe
            self.rect = self.image.get_rect(midtop=(pipe_x_pos, 0))

        self.speed = 3

    def destroy(self):
        if self.rect.x < -self.image.get_width():
            self.kill()

    def update(self):
        self.destroy()
        self.rect.x -= self.speed
