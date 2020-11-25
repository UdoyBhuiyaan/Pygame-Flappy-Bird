import pygame
import sys
import os


# Initialising game environment, screen size and clock tick rate
pygame.init()
screen = pygame.display.set_mode((576,1024))
clock = pygame.time.Clock()

# Game variables
gravity = 0.25
bird_move = 0


# Loading background assets
bg_path = 'git/Pygame/Flappy Bird/assets/background-day.png'
bg_surface = pygame.image.load(bg_path).convert()
bg_surface = pygame.transform.scale2x(bg_surface)

# Loading floor assets
floor_path = 'git/Pygame/Flappy Bird/assets/base.png'
floor_surface = pygame.image.load(floor_path).convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

# Loading bird assets
bird_path = 'git/Pygame/Flappy Bird/assets/bluebird-midflap.png'
bird_surface = pygame.image.load(bird_path).convert()
bird_surface = pygame.transform.scale2x(bird_surface)
bird_rect = bird_surface.get_rect(center = (100,512))


# Function to draw moving floor
def render_floor():
    screen.blit(floor_surface, (floor_x_pos,900))
    screen.blit(floor_surface, (floor_x_pos + 576,900))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_move -= 12

    screen.blit(bg_surface, (0,0))
    bird_move += gravity
    bird_rect.centery += bird_move
    screen.blit(bird_surface, bird_rect)
    floor_x_pos -= 1
    render_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0


    pygame.display.update()
    clock.tick(120)

