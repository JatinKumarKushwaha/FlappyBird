import sys
import os
import pygame
import json

from random import randrange
from threading import Thread, Event

from entities.bird import Bird
from entities.pipe import Pipe

from utils.input_box import InputBox
from utils.text import draw_text
from utils.button import Button
from utils.collision import collision_sprite

from utils.netcode.server_class import Server
from utils.netcode.client_class import Client

# Initialize pygame
pygame.init()

# Font
font = pygame.font.Font(
    "assets/fonts/Caskaydia_Cove_Nerd_Font_Complete_Regular.otf", 50
)

# Game title
window_title = "Flappy Bird"
pygame.display.set_caption(window_title)

# Screen space
screen_width = 900
screen_height = 480
resolution = (screen_width, screen_height)
screen = pygame.display.set_mode(resolution)

# Sky
sky = pygame.image.load("assets/graphics/sky.png").convert_alpha()

# Ground
ground = pygame.image.load("assets/graphics/ground.png").convert_alpha()

# Framerate clock
clock = pygame.time.Clock()

# Bird group
birdGroup = pygame.sprite.Group()

# Pipe group
pipeGroup = pygame.sprite.Group()

# Score
score = 0

# For online game
connection_complete = Event()
server_code_upate = Event()
address_already_in_use = Event()
code_temp = [1, 1, 1, 1, 1, 1]

# Look for flappy_bird.cfg file, if it's not there create one
if not (os.path.isfile("flappy_bird.cfg")):
    settings = {
        "Logging": False,
        "Resolution": "900x460",
        "High-Score": 0,
    }
    with open("flappy_bird.cfg", "w") as outfile:
        json.dump(settings, outfile)
# If it's there store data into a settings object
else:
    with open("flappy_bird.cfg", "r") as infile:
        settings = json.load(infile)


# Draw call
def redrawWindow(screen, entities):
    # Draw Sky
    screen.blit(sky, (0, 0))
    if screen_width - sky.get_width() > 0:
        screen.blit(sky, (screen_width - sky.get_width(), 0))
        screen.blit(
            ground,
            (screen_width - sky.get_width(), screen_height - ground.get_height()),
        )

    # Draw Ground
    screen.blit(ground, (0, screen_height - ground.get_height()))
    if screen_height - (ground.get_height() + sky.get_height()) > 0:
        screen.blit(ground, (0, sky.get_height()))

    # Draw player
    for entity in entities:
        entity.draw(screen)

    # Update frame
    pygame.display.update()


# Server
def server(code):
    server = Server()
    if not server.listen():
        address_already_in_use.set()
        return
    temp = server.getCode()
    for i in range(len(code)):
        code[i] = int(temp % 10)
        temp /= 10
    server_code_upate.set()

    clients = []
    i = 0
    while i != server.MAX_CLIENTS:
        (conn, addr) = server.accept()  # type: ignore

        clients.append((conn, addr))
        i += 1
        if not server.handShakeWithAddress(addr):
            return

        # Status 200 after handshake
        data_receive = server.receiveFromAddress(addr)
        if not data_receive == 200:
            print("Something's wrong")

    connection_complete.set()

    # Send client ids
    data = dict()
    for client in clients:
        server.sendToAddress(client[1], client[1])
        data[client[1]] = ""

    for client in clients:
        server.receiveFromAddress(client[1])

    # Send different start_pos and color to all players
    i = 0
    for client in clients:
        # start_pos -> (x, y)
        # color -> (r, g, b) | (r, g, b, a)
        data[client[1]] = [
            ((50, int(resolution[1] / 2 + (i * 3)))),
            ((55 + i * 10, 0 + i * 4, 255 - (i * 2), 255 - i * 10)),
        ]
        i += 10

    # First send
    server.sendAll(data)

    for client in clients:
        data[client[1]] = ""

    connection_alive = True

    # data = [pipe_data, {client_id: [player_input, game_over]}, {client_id: [player_input, game_over]}, ...]
    # player_input = True | False
    # gave_over = True | False
    # pipe_data = [pipe_type, pipe_x_pos]

    pipe_width = pygame.image.load("assets/graphics/pipe.png").get_width()

    data_packet = []

    pipe_type = randrange(0, 2)
    pipe_x_pos = randrange(resolution[0] + 100, resolution[0] + 500, pipe_width)
    pipe_data = [pipe_type, pipe_x_pos]

    data_packet.append(pipe_data)

    for client in clients:
        data[client[1]] = [False, True]
    data_packet.append(data)

    server.sendAll(data_packet)

    while connection_alive:
        data_packet = []
        recieved_data = {}

        for client in clients:
            # Recieve data from all the clients
            recieved_data[client[1]] = server.receiveFromAddress(client[1])[client[1]]  # type: ignore

        pipe_type = randrange(0, 2)
        pipe_x_pos = randrange(resolution[0] + 100, resolution[0] + 500, pipe_width)
        pipe_data = [pipe_type, pipe_x_pos]

        data_packet.append(pipe_data)

        for client in clients:
            data[client[1]] = recieved_data[client[1]]
        data_packet.append(data)

        server.sendAll(data_packet)


# Online game
def online_game(code, flag=False):
    if code == "":
        return

    client = Client()
    if not client.connect():
        return
    if not client.handShake(code):
        return

    backButton = Button(
        (resolution[0] / 2), (resolution[1] / 2) + 120, 300, 50, "Back", font
    )

    # Waiting for all connections
    while flag:
        if connection_complete.is_set():
            break
        screen.fill((0, 190, 255))
        draw_text(
            (resolution[0] / 2),
            (resolution[1] / 2) - 160,
            "Waiting for a connection...",
            font,
            (255, 255, 0),
            screen,
        )
        draw_text(
            (resolution[0] / 2),
            (resolution[1] / 2) - 20,
            "Server Code is: " + code,
            font,
            (255, 255, 0),
            screen,
        )

        backButton.update(screen)

        if backButton.isPressed():
            # Return to menu
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)

    # Get id and send response code
    client_id = client.recieve()
    client.send(200)

    data = client.recieve()  # type:ignore
    for key in data.keys():  # type:ignore
        id = key
        start_pos = data[key][0]
        color = data[key][1]
        birdGroup.add(
            Bird(resolution, id, start_pos[0], start_pos[1], color)  # type:ignore
        )

    start_time = int(pygame.time.get_ticks() / 1000)
    score = 0

    running = True
    game_active = True

    # Pipe timer
    pipe_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(pipe_timer, 1500)

    data = {}

    # Online Game
    while running:
        if not game_active:
            continue

        server_data = client.recieve()
        pipe_data = server_data[0]
        players = {}

        for data in server_data:
            if type(data) == dict:
                players.update(data)
        players[client_id][0] = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game_active and event.type == pipe_timer:
                pipeGroup.add(
                    Pipe(
                        resolution=resolution,
                        type=pipe_data[0],
                        pipe_x_pos=pipe_data[1],
                    )
                )

            # Handle input
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                players[client_id][0] = True

        for bird in birdGroup.sprites():
            if players[bird.getId()][0]:
                bird.jump()

        if game_active:
            # Draw Sky
            screen.blit(sky, (0, 0))
            if screen_width - sky.get_width() > 0:
                screen.blit(sky, (screen_width - sky.get_width(), 0))
                screen.blit(
                    ground,
                    (
                        screen_width - sky.get_width(),
                        screen_height - ground.get_height(),
                    ),
                )

            # Draw Ground
            screen.blit(ground, (0, screen_height - ground.get_height()))
            if screen_height - (ground.get_height() + sky.get_height()) > 0:
                screen.blit(ground, (0, sky.get_height()))

            # Brid
            birdGroup.draw(screen)
            birdGroup.update()

            # Pipe
            pipeGroup.draw(screen)
            pipeGroup.update()

            # Score
            score = display_score(start_time)

            # Store game_over data
            for bird in birdGroup.sprites():
                game_active = collision_sprite(bird, pipeGroup)
                if not game_active:
                    bird.kill()

            for key in players.keys():
                game_active = players[key][1]

            if len(birdGroup.sprites()) < 2:
                game_active = False
                birdGroup.empty()
                pipeGroup.empty()

            data[client_id] = [players[client_id][0], game_active]  # type:ignore
            client.send(data)
        else:
            # Show retry screen
            retry_screen(score)

            # Reset start time so score becomes zero
            start_time = int(pygame.time.get_ticks() / 1000)

            # Restart game
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                game_active = True
                if not birdGroup:
                    birdGroup.add(Bird(resolution=resolution, id=1, x=40, y=40))

            if keys[pygame.K_SPACE]:
                game_active = False
                running = False
                break

        pygame.display.update()
        clock.tick(60)


# Create server
def create_server():
    s = Thread(target=server, args=(code_temp,))
    s.daemon = True
    s.start()
    server_code = ""
    while not server_code_upate.is_set():
        if address_already_in_use.is_set():
            return ""
        continue
    for c in code_temp:
        server_code += str(c)
    server_code = server_code[::-1]

    return server_code


# Join Game
def join_game():
    backButton = Button(
        (resolution[0] / 2), (resolution[1] / 2) + 120, 300, 50, "Back", font
    )
    codeBox = InputBox((resolution[0] / 2), (resolution[1] / 2), 400, 100, font)
    ibg = pygame.sprite.Group(codeBox)  # type: ignore
    text = ""

    while True:
        screen.fill((0, 190, 255))
        draw_text(
            (resolution[0] / 2),
            (resolution[1] / 2) - 160,
            "Enter code",
            font,
            (255, 255, 0),
            screen,
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                text = codeBox.getText()
                return text
            ibg.update(event)

        # Display buttons
        backButton.update(screen)

        if backButton.isPressed():
            # Break out of the while loop
            break

        # Display text box
        ibg.draw(screen)

        pygame.display.update()
        clock.tick(60)
    return text


# Display score
def display_score(start_time):
    # pygame.time.get_ticks() -> gives time since pygame started in milisecond
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    draw_text(10, 0, f"{current_time}", font, (0, 0, 100), screen, "topleft")
    return current_time


# Retry Screen
def retry_screen(score):
    screen.fill((0, 0, 0))
    small_font = pygame.font.Font(
        "assets/fonts/Caskaydia_Cove_Nerd_Font_Complete_Regular.otf", 45
    )
    draw_text(
        (resolution[0] / 2),
        (resolution[1] / 2) - 160,
        f"{window_title}",
        font,
        (0, 0, 100),
        screen,
    )
    draw_text(
        (resolution[0] / 2),
        (resolution[1] / 2) + 40,
        f"Score: {score}",
        font,
        (144, 94, 38),
        screen,
    )
    draw_text(
        (resolution[0] / 2),
        (resolution[1] / 2) - 100,
        "Press Space to return to menu",
        small_font,
        (111, 196, 1),
        screen,
    )
    draw_text(
        (resolution[0] / 2),
        (resolution[1] / 2) + 160,
        "Press Enter to restart",
        font,
        (111, 196, 1),
        screen,
    )

    high_score = settings["High-Score"] | 0

    # Update high score
    if score > high_score:
        high_score = score
        settings["High-Score"] = high_score
        with open("flappy_bird.cfg", "w") as outfile:
            json.dump(settings, outfile)

    draw_text(
        (resolution[0] / 2),
        (resolution[1] / 2) + 100,
        f"HighScore: {high_score}",
        font,
        (183, 132, 112),
        screen,
    )


# Change game options
def options():
    backButton = Button(
        (resolution[0] / 2), (resolution[1] / 2) + 120, 300, 50, "Back", font
    )

    while True:
        screen.fill((0, 190, 255))
        draw_text(
            (resolution[0] / 2),
            (resolution[1] / 2) - 160,
            "Options",
            font,
            (255, 255, 0),
            screen,
        )

        # Display settings data
        i = 0
        for setting in settings:
            draw_text(
                (resolution[0] / 2) - 200,
                (resolution[1] / 2) - 100 + i,
                str(setting),
                font,
                (0, 0, 0),
                screen,
            )
            draw_text(
                (resolution[0] / 2) + 200,
                (resolution[1] / 2) - 100 + i,
                str(settings[setting]),
                font,
                (0, 0, 0),
                screen,
            )
            i += 60

        backButton.update(screen)

        if backButton.isPressed():
            # Break out of the while loop
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)

    # Return to the main function after the break, so as to not casue an infinite recursion
    return


# Show info on how to play
def howToPlay():
    backButton = Button(
        (resolution[0] / 2), (resolution[1] / 2) + 100, 300, 50, "Back", font
    )

    while True:
        screen.fill((0, 190, 255))
        draw_text(
            (resolution[0] / 2),
            (resolution[1] / 2) - 160,
            "How to play",
            font,
            (255, 255, 0),
            screen,
        )
        draw_text(
            (resolution[0] / 2),
            (resolution[1] / 2) - 100,
            "Just use the Space button",
            font,
            (0, 0, 0),
            screen,
        )

        backButton.update(screen)

        if backButton.isPressed():
            # Break out of the while loop
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)

    # Return to the main function after the break, so as to not casue an infinite recursion
    return


# Play offline/single player
def offline_game():
    start_time = int(pygame.time.get_ticks() / 1000)
    score = 0

    # Game active
    game_active = True
    running = True

    # Bird
    birdGroup.add(
        Bird(
            resolution=resolution,
            id=1,
            x=50,
            y=int(resolution[1] / 2),
        )
    )

    pipe_width = pygame.image.load("assets/graphics/pipe.png").get_width()

    # Pipe timer
    pipe_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(pipe_timer, 1500)

    # Main game loop
    while running:
        # Exit game when user exits
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game_active:
                if event.type == pipe_timer:
                    pipeGroup.add(
                        Pipe(
                            resolution,
                            randrange(0, 2),
                            randrange(
                                resolution[0] + 100, resolution[0] + 500, pipe_width
                            ),
                        )
                    )
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    for bird in birdGroup.sprites():
                        bird.jump()

        if game_active:
            # Draw Sky
            screen.blit(sky, (0, 0))
            if screen_width - sky.get_width() > 0:
                screen.blit(sky, (screen_width - sky.get_width(), 0))
                screen.blit(
                    ground,
                    (
                        screen_width - sky.get_width(),
                        screen_height - ground.get_height(),
                    ),
                )

            # Draw Ground
            screen.blit(ground, (0, screen_height - ground.get_height()))
            if screen_height - (ground.get_height() + sky.get_height()) > 0:
                screen.blit(ground, (0, sky.get_height()))

            # Brid
            birdGroup.draw(screen)
            birdGroup.update()

            # Pipe
            pipeGroup.draw(screen)
            pipeGroup.update()

            # Score
            score = display_score(start_time)

            for bird in birdGroup.sprites():
                game_active = collision_sprite(bird, pipeGroup)

            if not birdGroup:
                game_active = False
                birdGroup.empty()
                pipeGroup.empty()

        else:
            # Show retry screen
            retry_screen(score)

            # Reset start time so score becomes zero
            start_time = int(pygame.time.get_ticks() / 1000)

            # Restart game
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                game_active = True
                if not birdGroup:
                    birdGroup.add(Bird(resolution=resolution, id=1, x=40, y=40))
            if keys[pygame.K_SPACE]:
                game_active = False
                running = False
                break

        # Update frame
        pygame.display.update()

        # Framerate
        clock.tick(60)
    return


# Play multiplayer
def online():
    join_gameButton = Button(
        (resolution[0] / 2) - 200, (resolution[1] / 2) - 80, 380, 60, "Join Game", font
    )
    createServerButton = Button(
        (resolution[0] / 2) + 200,
        (resolution[1] / 2) - 80,
        380,
        60,
        "Create Server",
        font,
    )
    backButton = Button(
        (resolution[0] / 2), (resolution[1] / 2) + 120, 300, 50, "Back", font
    )

    while True:
        screen.fill((0, 190, 255))
        draw_text(
            (resolution[0] / 2),
            (resolution[1] / 2) - 160,
            window_title,
            font,
            (255, 255, 0),
            screen,
        )

        # Display buttons
        join_gameButton.update(screen)
        createServerButton.update(screen)
        backButton.update(screen)

        if join_gameButton.isPressed():
            code = join_game()
            online_game(code)
        if createServerButton.isPressed():
            code = create_server()
            online_game(code, True)
        if backButton.isPressed():
            # Break out of the while loop
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)

    # Return to the main function after the break, so as to not casue an infinite recursion
    return


# Main menu
def main():
    playButton = Button(
        (resolution[0] / 2), (resolution[1] / 2) - 80, 360, 60, "Play Offline", font
    )
    onlinePlayButton = Button(
        (resolution[0] / 2), (resolution[1] / 2), 360, 60, "Play Online", font
    )
    optionsButton = Button(
        (resolution[0] / 2), (resolution[1] / 2) + 80, 360, 60, "Options", font
    )
    howToPlayButton = Button(
        (resolution[0] / 2), (resolution[1] / 2) + 160, 360, 60, "How to play", font
    )

    # Show main menu
    while True:

        screen.fill((0, 190, 255))
        draw_text(
            (resolution[0] / 2),
            (resolution[1] / 2) - 160,
            window_title,
            font,
            (255, 255, 0),
            screen,
        )

        # Display buttons
        playButton.update(screen)
        optionsButton.update(screen)
        howToPlayButton.update(screen)
        onlinePlayButton.update(screen)

        if playButton.isPressed():
            offline_game()
        if optionsButton.isPressed():
            options()
        if howToPlayButton.isPressed():
            howToPlay()
        if onlinePlayButton.isPressed():
            online()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
