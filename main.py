import sys
import pygame
from random import randint
from bird import Bird
from obstacles import Obstacles
from utils import collision_sprite

def main():
	# Initialize pygame
	pygame.init()

	# Font
	font = pygame.font.Font('assets/fonts/Caskaydia_Cove_Nerd_Font_Complete_Regular.otf', 50)

	# Game title
	window_title = 'Flappy Bird'
	pygame.display.set_caption(window_title)

	# Screen space
	screen_width = 800
	screen_height = 400
	resolution = (screen_width, screen_height)
	screen = pygame.display.set_mode(resolution)

	# Game active
	game_active = True

	# Sky
	sky = pygame.image.load('assets/graphics/sky.png').convert_alpha()

	# Ground
	ground = pygame.image.load('assets/graphics/ground.png').convert_alpha()

	# Framerate clock
	clock = pygame.time.Clock()

	# Bird group
	bird = pygame.sprite.GroupSingle()
	bird.add(Bird(resolution=resolution))

	# Pipe group
	pipe = pygame.sprite.Group()

	# Time
	start_time = 0

	# Score
	score = 0

	def display_score():
		# pygame.time.get_ticks() -> gives time since pygmae started in milisecond
		current_time = int(pygame.time.get_ticks() / 1000) - start_time
		score_surface = font.render(f'{current_time}', False, (0, 0, 100))
		score_rect = score_surface.get_rect(topleft = (10, 0))
		screen.blit(score_surface, score_rect)
		return current_time

	# Retry Screen
	def retry_screen():
		game_title = font.render(f'{window_title}', False, (0, 0, 100))
		game_title_rect = game_title.get_rect(center = (int(screen_width / 2), int(screen_height / 2) - 110))
		score_message = font.render(f'Score: {score}', False, (144, 94, 38))
		score_message_rect = score_message.get_rect(center = (int(screen_width / 2), int(screen_height / 2) - 50))

		f = open("assets/highscore", "r+")
		high_score = int(f.read())
		f.close()
		# Update high score
		if score > high_score:
			high_score = score
			f = open("assets/highscore", "w+")
			f.write(str(high_score))
			f.close()

		high_score_message = font.render(f'HighScore: {high_score}', False, (183, 132, 112))
		high_score_message_rect = high_score_message.get_rect(center = (int(screen_width / 2), screen_height - 100))
		game_message = font.render('Press Enter to restart', False, (111, 196, 1))
		game_message_rect = game_message.get_rect(center = (int(screen_width / 2), screen_height - 40))

		screen.fill((0, 0, 0))
		screen.blit(score_message, score_message_rect)
		screen.blit(high_score_message, high_score_message_rect)
		screen.blit(game_title, game_title_rect)
		screen.blit(game_message, game_message_rect)

	# Pipe timer
	obstacle_timer = pygame.USEREVENT + 1
	pygame.time.set_timer(obstacle_timer, 1500)

	# Main game loop
	while True:
		# Exit game when user exits
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if game_active:
				if event.type == obstacle_timer:
					pipe.add(Obstacles(resolution=resolution,type=randint(0, 1)))

		if game_active:
			# Draw Sky
			screen.blit(sky, (0, 0))
			if screen_width - sky.get_width() > 0:
				screen.blit(sky, (screen_width - sky.get_width(), 0))
				screen.blit(ground, (screen_width - sky.get_width(), screen_height - ground.get_height()))

			# Draw Ground
			screen.blit(ground, (0, screen_height - ground.get_height()))
			if screen_height - (ground.get_height() + sky.get_height()) > 0:
				screen.blit(ground, (0, sky.get_height()))

			# Brid
			bird.draw(screen)
			bird.update()

			# Pipe
			pipe.draw(screen)
			pipe.update()

			# Score
			score = display_score()

			game_active = collision_sprite(bird, pipe)

			if bird.sprite == None:
				game_active = False
				pipe.empty()
		else:
			# Show retry screen
			retry_screen()

			# Reset start time so score becomes zero
			start_time = int(pygame.time.get_ticks() / 1000)

			# Restart game
			keys = pygame.key.get_pressed()
			if keys[pygame.K_RETURN]:
				game_active = True
				if bird.sprite == None:
					bird.add(Bird(resolution=resolution))

		# Update frame
		pygame.display.update()
		
		# Framerate
		clock.tick(60)
	

if __name__ == "__main__":
	main()
