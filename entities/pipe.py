import pygame


class Pipe(pygame.sprite.Sprite):
    def __init__(self, resolution, type, pipe_x_pos, pipe_y_pos):
        super().__init__()

        # Screen resolution format: tuple(width, height)
        self.resolution = resolution

        # Pipe
        self.pipe = pygame.image.load("assets/graphics/pipe.png").convert_alpha()
        self.pipe = pygame.transform.rotozoom(self.pipe, 0, 1.0)

        # Upsidedown Pipe
        self.upsidedown_pipe = pygame.image.load(
            "assets/graphics/pipe.png"
        ).convert_alpha()
        self.upsidedown_pipe = pygame.transform.rotozoom(self.pipe, 180, 1.0)

        if type:
            self.image = self.pipe
            self.rect = self.image.get_rect(midtop=(pipe_x_pos, pipe_y_pos + 200))
        else:
            self.image = self.upsidedown_pipe
            self.rect = self.image.get_rect(midbottom=(pipe_x_pos, pipe_y_pos))

        self.speed = 3

    def destroy(self):
        if self.rect.x < -1 * self.image.get_width():
            self.kill()

    def update(self):
        self.destroy()
        self.rect.x -= self.speed
