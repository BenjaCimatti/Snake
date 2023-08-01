# import os
# os.environ["SDL_VIDEODRIVER"]="x11"
import pygame
from pygame.locals import * # import all the modules from pygame

clock = pygame.time.Clock()

pygame.init() # initiates pygame

WINDOW_SIZE = (400,400)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32) # initiates the window
pygame.display.set_caption('Snake')

head_color = (6,157,87)
head_size = (15,15)
head_coord = [WINDOW_SIZE[0]/2 - head_size[0]/2, WINDOW_SIZE[1]/2 - head_size[1]/2]

directions = ('right', 'left', 'up', 'down')
direction = directions[3]

def movement(direction):
    if direction == 'right':
        head_coord[0] += head_size[0]
    if direction == 'left':
        head_coord[0] -= head_size[0]
    if direction == 'up':
        head_coord[1] -= head_size[0]
    if direction == 'down':
        head_coord[1] += head_size[0]

start_time = pygame.time.get_ticks()
open = True
while open: # game loop
    for event in pygame.event.get(): # event loop
        if event.type == QUIT:
            pygame.quit()
            open = False
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                direction = directions[0]
            if event.key == K_LEFT:
                direction = directions[1]
            if event.key == K_UP:
                direction = directions[2]
            if event.key == K_DOWN:
                direction = directions[3]
    
    screen.fill((137,245,195))
    pygame.draw.rect(screen, head_color, pygame.Rect(head_coord,head_size))

    current_time = pygame.time.get_ticks()
    if current_time - start_time >= 100:
        movement(direction)
        start_time = current_time
    
    
    pygame.display.update()
    clock.tick(60) # window framerate