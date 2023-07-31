# import os
# os.environ["SDL_VIDEODRIVER"]="x11"
import pygame
from pygame.locals import * # import all the modules from pygame

clock = pygame.time.Clock()

pygame.init() # initiates pygame

WINDOW_SIZE = (400,400)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32) # initiates the window
pygame.display.set_caption('Snake')


open = True

while open: # game loop
    for event in pygame.event.get(): # event loop
        if event.type == QUIT:
            pygame.quit()
            open = False
    
    pygame.display.update()
    clock.tick(60) # window framerate