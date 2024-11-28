import pygame
from utils.color import tint


class Bird(pygame.sprite.Sprite):
    def __init__(self, resolution, id, x=40, y=40, color=(0, 0, 0, 0)):
        super().__init__()

        # Screen resolution format: tuple(width, height)
        self.resolution = resolution
        self.id = id
        self.x = x
        self.y = y
        self.color = color

        # Load bird image
        self.bird = pygame.image.load("assets/graphics/brid/bird.png").convert_alpha()
        self.bird = pygame.transform.rotozoom(self.bird, 0, 0.06)
        if not self.color == (0, 0, 0, 0):
            self.bird = tint(self.bird, color)

        # Jump image
        self.bird_jump = pygame.image.load(
            "assets/graphics/brid/bird.png"
        ).convert_alpha()
        self.bird_jump = pygame.transform.rotozoom(self.bird_jump, 30, 0.06)
        if not self.color == (0, 0, 0, 0):
            self.bird_jump = tint(self.bird_jump, color)

        self.image = self.bird
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # Gravity
        self.gravity = 0

        # Jump sound
        self.jump_sound = pygame.mixer.Sound("assets/audio/jump.wav")
        self.jump_sound.set_volume(0.5)

    def getId(self):
        return self.id

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.gravity = -2
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 0.1
        self.rect.y += int(self.gravity)

    def animate(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.image = self.bird_jump
        else:
            self.image = self.bird

    def destroy(self):
        if self.rect.y > self.resolution[1] or self.rect.y < 0:
            self.kill()

    def jump(self):
        self.gravity = -2
        self.jump_sound.play()

    def update(self):
        self.animate()
        self.apply_gravity()
        self.destroy()
