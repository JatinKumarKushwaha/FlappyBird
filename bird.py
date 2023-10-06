import pygame

class Bird(pygame.sprite.Sprite):
	def __init__(self, resolution):
		super().__init__()

		# Screen resolution format: tuple(width, height)
		self.resolution = resolution

		# Load bird image
		self.bird = pygame.image.load('assets/graphics/brid/bird.png').convert_alpha()
		self.bird = pygame.transform.rotozoom(self.bird, 0, 0.06)
		
		# Jump image
		self.bird_jump = pygame.image.load('assets/graphics/brid/bird.png').convert_alpha()
		self.bird_jump = pygame.transform.rotozoom(self.bird_jump, 30, 0.06)

		self.image = self.bird
		self.rect = self.image.get_rect(center = (self.image.get_width(), self.resolution[1] / 2))
		self.gravity = 0
		self.jump_sound = pygame.mixer.Sound('assets/audio/jump.wav')
		self.jump_sound.set_volume(0.5)
	
	def input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE]:
			self.gravity = -2
			self.jump_sound.play()

	
	def apply_gravity(self):
		self.gravity += 0.1
		self.rect.y += self.gravity

	def animation(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE]:
			self.image = self.bird_jump
		else:
			self.image = self.bird

	def destroy(self):
		if self.rect.y > self.resolution[1] or self.rect.y < 0:
			self.kill()

	def update(self):
		self.input()
		self.animation()
		self.apply_gravity()
		self.destroy()