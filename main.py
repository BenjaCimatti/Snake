import pygame, random, sys
from pygame.math import Vector2
from pygame.locals import *

class Fruit:
    def __init__(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)
        

class Snake:
    def __init__(self):
        self.body = [Vector2(7,10), Vector2(6,10), Vector2(5,10)]
        self.direction = Vector2(1,0)
    
    def draw_snake(self):
        for vector in self.body:
            block_rect = pygame.Rect(int(vector.x * cell_size), int(vector.y * cell_size), cell_size, cell_size)
            pygame.draw.rect(screen, (6,157,87), block_rect) 
    
    def move_snake(self):
        body_copy = self.body[:-1]
        body_copy.insert(0, self.body[0] + self.direction)
        self.body = body_copy

class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
        self.start_time = pygame.time.get_ticks()
    
    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= 100:
            self.snake.move_snake()
            self.start_time = current_time
            self.check_fruit_collision()
            self.check_game_over()

    def check_fruit_collision(self):
        if self.snake.body[0] == self.fruit.pos:
            self.fruit = Fruit()
            tail = self.snake.body[-1]
            self.snake.body.append(tail)

    def check_game_over(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        pygame.quit()
        sys.exit()



pygame.init() # initiates pygame
cell_number = 20
cell_size = 20
WINDOW_SIZE = (cell_number * cell_size, cell_number * cell_size)
screen = pygame.display.set_mode(WINDOW_SIZE) # initiates the window
clock = pygame.time.Clock()
pygame.display.set_caption('Snake')
apple = pygame.image.load('assets/apple.png').convert_alpha()

main_game = Main()

previous_direc = main_game.snake.direction
r_move = Vector2(1,0)
l_move = Vector2(-1,0)
u_move = Vector2(0,-1)
d_move = Vector2(0,1)

start_time = pygame.time.get_ticks()
open = True
while open: # game loop
    for event in pygame.event.get(): # event loop
        if event.type == QUIT:
            pygame.quit()
            open = False
        if event.type == KEYDOWN:
            previous_direc = main_game.snake.direction
            if event.key == K_RIGHT:
                if previous_direc != l_move:
                    main_game.snake.direction = r_move
            if event.key == K_LEFT:
                if previous_direc != r_move:
                    main_game.snake.direction = l_move
            if event.key == K_UP:
                if previous_direc != d_move:
                    main_game.snake.direction = u_move
            if event.key == K_DOWN:
                if previous_direc != u_move:
                    main_game.snake.direction = d_move
    
    screen.fill((175, 215, 70))
    main_game.draw_elements()

    current_time = main_game.update()

    pygame.display.update()
    clock.tick(60) # window framerate