import pygame
import sys
import random

# Initialising game environment
pygame.init()

# Establish screen size, clock tick rate and game variables
screen_width = 576
screen_height = 1024
floor_height = 900
sky_upper_limit = -100
pipe_gap = 250
pipe_speed = 5
pipe_refresh_rate = 1200
move_speed = 10
gravity = 0.25
bird_move = 0
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
game_active = True

# Loading background assets
bg_path = 'assets/background-day.png'
bg_surface = pygame.image.load(bg_path).convert()
bg_surface = pygame.transform.scale2x(bg_surface)

# Loading floor assets
floor_path = 'assets/base.png'
floor_surface = pygame.image.load(floor_path).convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

# Loading bird assets
bird_path = 'assets/bluebird-midflap.png'
bird_surface = pygame.image.load(bird_path).convert()
bird_surface = pygame.transform.scale2x(bird_surface)
bird_rect = bird_surface.get_rect(center = (100,screen_height/2))

# Load pipe assets
pipe_path = 'assets/pipe-green.png'
pipe_surface = pygame.image.load(pipe_path).convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)

# Pipe variables for random heights and to generate new pipes
# every 1200ms.
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, pipe_refresh_rate)
pipe_height = range(400, 800, 100)

# Function to render moving floor
def render_floor():
    screen.blit(floor_surface, (floor_x_pos,floor_height))
    screen.blit(floor_surface, (floor_x_pos + screen_width, floor_height))

# Function to create top and bottom pipes with random heights, 
# adding 50 to width to generate pipe off screen
def create_pipe():
    random_pipe_height = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (screen_width + 50, random_pipe_height))
    top_pipe = pipe_surface.get_rect(midbottom = (screen_width + 50, random_pipe_height - pipe_gap))
    return bottom_pipe, top_pipe

# Function to move the pipes from right to left
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= pipe_speed
    return pipes

# Function to render pipes with inversions for top pipes
def render_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= screen_height:
            screen.blit(pipe_surface, pipe)
        else: 
            flipped_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flipped_pipe, pipe)

# Function to check for rect (rectangle) collisions
def check_collisions(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= sky_upper_limit or bird_rect.bottom >= floor_height:
        return False
    return True

# Main game loop
while True:
    for event in pygame.event.get():
        # Exit game loop with user quit
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Check for spacebar inputs, to play the game while active and to reset 
        # the game upon game over
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_move = 0
                bird_move -= move_speed
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, screen_height/2)
                bird_move = 0
        # Spawn new pipe using create_pipe function
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

    # Render background
    screen.blit(bg_surface, (0,0))

    # Active game checker based off collision rules
    if game_active == True:
        # Bird functionality
        bird_move += gravity
        bird_rect.centery += bird_move
        screen.blit(bird_surface, bird_rect)
        game_active = check_collisions(pipe_list)

        # Pipe generation
        pipe_list = move_pipes(pipe_list)
        render_pipes(pipe_list)

    # Looping floor animation
    floor_x_pos -= 1
    render_floor()
    if floor_x_pos <= -screen_width:
        floor_x_pos = 0


    pygame.display.update()
    clock.tick(120)

