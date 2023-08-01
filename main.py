import pygame, random
from pygame.math import Vector2
from pygame.locals import *

class Fruit:
    def __init__(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        pygame.draw.rect(screen, (255,0,0), fruit_rect)

class Snake:
    def __init__(self):
        pass

clock = pygame.time.Clock()

pygame.init() # initiates pygame
cell_number = 20
cell_size = 20

WINDOW_SIZE = (cell_number * cell_size, cell_number * cell_size)

screen = pygame.display.set_mode(WINDOW_SIZE) # initiates the window
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

fruit = Fruit()

start_time = pygame.time.get_ticks()
open = True
while open: # game loop
    for event in pygame.event.get(): # event loop
        if event.type == QUIT:
            pygame.quit()
            open = False
        if event.type == KEYDOWN:
            previous_direc = direction
            if event.key == K_RIGHT:
                if previous_direc != 'left':
                    direction = directions[0]
            if event.key == K_LEFT:
                if previous_direc != 'right':
                    direction = directions[1]
            if event.key == K_UP:
                if previous_direc != 'down':
                    direction = directions[2]
            if event.key == K_DOWN:
                if previous_direc != 'up':
                    direction = directions[3]
    
    screen.fill((175, 215, 70))
    fruit.draw_fruit()
    pygame.draw.rect(screen, head_color, pygame.Rect(head_coord,head_size))

    current_time = pygame.time.get_ticks()
    if current_time - start_time >= 100:
        movement(direction)
        start_time = current_time
    
    pygame.display.update()
    clock.tick(60) # window framerate