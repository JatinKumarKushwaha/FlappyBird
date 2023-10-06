import pygame
from random import randrange

class Obstacles(pygame.sprite.Sprite):
	def __init__(self, resolution, type):
		super().__init__()

		# Screen resolution format: tuple(width, height)
		self.resolution = resolution

		# Normal pipe
		self.pipe = pygame.image.load('assets/graphics/normal_pipe.png').convert_alpha()
		self.pipe = pygame.transform.rotozoom(self.pipe, 0, 1.0)
		
		# Upsidedown pipe
		self.opposite_pipe = pygame.image.load('assets/graphics/opposite_pipe.png').convert_alpha()
		self.opposite_pipe = pygame.transform.rotozoom(self.opposite_pipe, 0, 1.0)

		if type:
			self.image = self.pipe
			self.rect = self.image.get_rect(midbottom = (randrange(self.resolution[0] + 100, self.resolution[0] + 500, self.image.get_width()), self.resolution[1]))
		else:
			self.image = self.opposite_pipe
			self.rect = self.image.get_rect(midtop = (randrange(self.resolution[0] + 100, self.resolution[0] + 500, self.image.get_width()), 0))

		self.speed = 3

	def destroy(self):
		if self.rect.x < -self.image.get_width():
			self.kill()

	def update(self):
		self.destroy()
		self.rect.x -= self.speed