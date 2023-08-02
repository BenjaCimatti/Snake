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
        self.body = [Vector2(5,10), Vector2(6,10), Vector2(7,10)]
        self.direction = Vector2(0,1)
    
    def draw_snake(self):
        for vector in self.body:
            block_rect = pygame.Rect(int(vector.x * cell_size), int(vector.y * cell_size), cell_size, cell_size)
            pygame.draw.rect(screen, (6,157,87), block_rect) 
    
    def move_snake(self):
        body_copy = self.body[:-1]
        body_copy.insert(0, self.body[0] + self.direction)
        self.body = body_copy

clock = pygame.time.Clock()

pygame.init() # initiates pygame
cell_number = 20
cell_size = 20

WINDOW_SIZE = (cell_number * cell_size, cell_number * cell_size)

screen = pygame.display.set_mode(WINDOW_SIZE) # initiates the window
pygame.display.set_caption('Snake')

fruit = Fruit()
snake = Snake()

start_time = pygame.time.get_ticks()
open = True
while open: # game loop
    for event in pygame.event.get(): # event loop
        if event.type == QUIT:
            pygame.quit()
            open = False
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                snake.direction = Vector2(1,0)
            if event.key == K_LEFT:
                snake.direction = Vector2(-1,0)
            if event.key == K_UP:
                snake.direction = Vector2(0,-1)
            if event.key == K_DOWN:
                snake.direction = Vector2(0,1)
    
    screen.fill((175, 215, 70))
    fruit.draw_fruit()
    snake.draw_snake()

    current_time = pygame.time.get_ticks()
    if current_time - start_time >= 100:
        snake.move_snake()
        start_time = current_time
    
    pygame.display.update()
    clock.tick(60) # window framerate