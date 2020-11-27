import pygame
import sys
import random

# Initialising game environment
pygame.init()

# Establish screen size, clock tick rate and game variables
screen_width = 576
screen_height = 1024
floor_height = 912
sky_upper_limit = -100
pipe_gap = 300
pipe_speed = 5
pipe_refresh_rate = 1000
jump_height = 10
gravity = 0.25
bird_movement = 0
score = 0
high_score = 0
game_font = pygame.font.Font('font.TTF', 40)
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
bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100,screen_height/2))

# Animation to flap the wings
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 25)

# Load pipe assets
pipe_path = 'assets/pipe-green.png'
pipe_surface = pygame.image.load(pipe_path).convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)

# Pipe variables for random heights and to generate new pipes
# every 1200ms.
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, pipe_refresh_rate)
pipe_height = range(400, 900, 50)

# Loading game over screen assets
game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (screen_width/2, screen_height/2))

# Loading sound assets
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
impact_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100

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
            impact_sound.play()
            return False
    if bird_rect.top <= sky_upper_limit or bird_rect.bottom >= floor_height:
        return False
    return True

# Function to rotate bird based on movement
def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird

# Function to cycle through bird_frames to simulate animation
def bird_animate():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect

# Function to display score and high score
def display_score(game_state):
    if game_state == 'active_game':
        score_surface = game_font.render(str(int(score)), True, (255,255,255))
        score_rect = score_surface.get_rect(center = (288, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255,255,255))
        score_rect = score_surface.get_rect(center = (288, 100))
        screen.blit(score_surface, score_rect)
        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (288, 850))
        screen.blit(high_score_surface, high_score_rect)

# Function to update high score
def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


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
                bird_movement = 0
                bird_movement -= jump_height
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, screen_height/2)
                bird_movement = 0
                score = 0
        # Spawn new pipe using create_pipe function
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animate()

    # Render background
    screen.blit(bg_surface, (0,0))

    # Active game checker based off collision rules
    if game_active == True:
        # Bird functionality
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collisions(pipe_list)

        # Pipe generation
        pipe_list = move_pipes(pipe_list)
        render_pipes(pipe_list)

        # Play sound every time score updates
        score += 0.01
        display_score('active_game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        display_score('game_over')

    # Looping floor animation
    floor_x_pos -= 1
    render_floor()
    if floor_x_pos <= -screen_width:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)

