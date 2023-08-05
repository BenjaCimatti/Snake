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
        self.step = Vector2(1,0)
        self.head = 'right'
    
    def draw_snake(self):
        self.update_head()
        for index, block in enumerate(self.body):
            block_rect = pygame.Rect(int(block.x * cell_size), int(block.y * cell_size), cell_size, cell_size)
            prev_block = self.body[index-1]

            if index == 0:
                if self.head == 'right':
                    screen.blit(spritesheet.get_image(cell_size, cell_size, 1), block_rect)
                elif self.head == 'left':
                    screen.blit(spritesheet.get_image(cell_size, cell_size, 3), block_rect)
                elif self.head == 'up':
                    screen.blit(spritesheet.get_image(cell_size, cell_size, 0), block_rect)
                elif self.head == 'down':
                    screen.blit(spritesheet.get_image(cell_size, cell_size, 2), block_rect)

            elif index == len(self.body) - 1:
                if prev_block.x > block.x:
                    screen.blit(spritesheet.get_image(cell_size, cell_size, 7), block_rect)
                elif prev_block.x < block.x:
                    screen.blit(spritesheet.get_image(cell_size, cell_size, 9), block_rect)
                elif prev_block.y > block.y:
                    screen.blit(spritesheet.get_image(cell_size, cell_size, 8), block_rect)
                elif prev_block.y < block.y:
                    screen.blit(spritesheet.get_image(cell_size, cell_size, 6), block_rect)
            
            else:
                next_block = self.body[index+1]

                if (prev_block.x < block.x and next_block.y > block.y) or (next_block.x < block.x and prev_block.y > block.y):
                    screen.blit(spritesheet.get_image(cell_size, cell_size, 10), block_rect)
                if (prev_block.x < block.x and next_block.y < block.y) or (next_block.x < block.x and prev_block.y < block.y):
                    screen.blit(spritesheet.get_image(cell_size, cell_size, 11), block_rect)
                if (prev_block.x > block.x and next_block.y < block.y) or (next_block.x > block.x and prev_block.y < block.y):
                    screen.blit(spritesheet.get_image(cell_size, cell_size, 12), block_rect)
                if (prev_block.x > block.x and next_block.y > block.y) or (next_block.x > block.x and prev_block.y > block.y):
                    screen.blit(spritesheet.get_image(cell_size, cell_size, 13), block_rect)

                if prev_block.y == block.y == next_block.y:
                    screen.blit(spritesheet.get_image(cell_size, cell_size, 5),block_rect)
                if prev_block.x == block.x == next_block.x:
                    screen.blit(spritesheet.get_image(cell_size, cell_size, 4),block_rect)
                
    def update_head(self):
        head_relation = self.body[0] - self.body[1]
        if head_relation == Vector2(1,0): self.head = 'right'
        if head_relation == Vector2(-1,0): self.head = 'left'
        if head_relation == Vector2(0,1): self.head = 'down'
        if head_relation == Vector2(0,-1): self.head = 'up'


    def move_snake(self):
        if main_game.check_fruit_collision():
            self.body.insert(0, self.body[0] + self.step)
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, self.body[0] + self.step)
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
            #self.check_fruit_collision()
            self.check_game_over()
            self.start_time = current_time

    def check_fruit_collision(self):
        if self.snake.body[0] == self.fruit.pos:
            self.fruit = Fruit()
            return True
        return False

    def check_game_over(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        pygame.quit()
        sys.exit()

class Spritesheet:
    def __init__(self, path):
        self.path = path
        self.spritesheet = pygame.image.load(path).convert_alpha()

    def get_image(self, width, height, frame):
        image = pygame.Surface((width, height)).convert_alpha()
        frame_rect = pygame.Rect(frame * width, 0, width, height)
        image.blit(self.spritesheet, (0,0), frame_rect)
        image.set_colorkey('black')

        return image
    
pygame.init() # initiates pygame
cell_number = 20
cell_size = 16
WINDOW_SIZE = (cell_number * cell_size, cell_number * cell_size)
screen = pygame.display.set_mode(WINDOW_SIZE) # initiates the window
clock = pygame.time.Clock()
pygame.display.set_caption('Snake')
apple = pygame.image.load('assets/apple.png').convert_alpha()

main_game = Main()

previous_direc = main_game.snake.step
r_move = Vector2(1,0)
l_move = Vector2(-1,0)
u_move = Vector2(0,-1)
d_move = Vector2(0,1)

start_time = pygame.time.get_ticks()
spritesheet = Spritesheet('assets/snake_sprite.png')

open = True
while open: # game loop
    for event in pygame.event.get(): # event loop
        if event.type == QUIT:
            open = False
        if event.type == KEYDOWN:
            previous_direc = main_game.snake.step
            if event.key == K_RIGHT:
                if previous_direc != l_move:
                    main_game.snake.step = r_move
            if event.key == K_LEFT:
                if previous_direc != r_move:
                    main_game.snake.step = l_move
            if event.key == K_UP:
                if previous_direc != d_move:
                    main_game.snake.step = u_move
            if event.key == K_DOWN:
                if previous_direc != u_move:
                    main_game.snake.step = d_move
    
    screen.fill((175, 215, 70))

    main_game.draw_elements()

    current_time = main_game.update()

    pygame.display.update()
    clock.tick(60) # window framerate

pygame.quit()