import pygame, random, sys
from pygame.math import Vector2
from pygame.locals import *

class Fire:
    def __init__(self):
        self.change_location()
        self.image = pygame.image.load('assets/fire.png').convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 2)

    def change_location(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

    def draw_fire(self):
        fire_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        field.blit(self.image, fire_rect)
        
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
                    field.blit(spritesheet.get_image(16, 16, 1), block_rect)
                elif self.head == 'left':
                    field.blit(spritesheet.get_image(16, 16, 3), block_rect)
                elif self.head == 'up':
                    field.blit(spritesheet.get_image(16, 16, 0), block_rect)
                elif self.head == 'down':
                    field.blit(spritesheet.get_image(16, 16, 2), block_rect)

            elif index == len(self.body) - 1:
                if prev_block.x > block.x:
                    field.blit(spritesheet.get_image(16, 16, 7), block_rect)
                elif prev_block.x < block.x:
                    field.blit(spritesheet.get_image(16, 16, 9), block_rect)
                elif prev_block.y > block.y:
                    field.blit(spritesheet.get_image(16, 16, 8), block_rect)
                elif prev_block.y < block.y:
                    field.blit(spritesheet.get_image(16, 16, 6), block_rect)
            
            else:
                next_block = self.body[index+1]

                if (prev_block.x < block.x and next_block.y > block.y) or (next_block.x < block.x and prev_block.y > block.y):
                    field.blit(spritesheet.get_image(16, 16, 10), block_rect)
                if (prev_block.x < block.x and next_block.y < block.y) or (next_block.x < block.x and prev_block.y < block.y):
                    field.blit(spritesheet.get_image(16, 16, 11), block_rect)
                if (prev_block.x > block.x and next_block.y < block.y) or (next_block.x > block.x and prev_block.y < block.y):
                    field.blit(spritesheet.get_image(16, 16, 12), block_rect)
                if (prev_block.x > block.x and next_block.y > block.y) or (next_block.x > block.x and prev_block.y > block.y):
                    field.blit(spritesheet.get_image(16, 16, 13), block_rect)

                if prev_block.y == block.y == next_block.y:
                    field.blit(spritesheet.get_image(16, 16, 5),block_rect)
                if prev_block.x == block.x == next_block.x:
                    field.blit(spritesheet.get_image(16, 16, 4),block_rect)
                
    def update_head(self):
        head_relation = self.body[0] - self.body[1]
        if head_relation == Vector2(1,0): self.head = 'right'
        if head_relation == Vector2(-1,0): self.head = 'left'
        if head_relation == Vector2(0,1): self.head = 'down'
        if head_relation == Vector2(0,-1): self.head = 'up'


    def move_snake(self):
        if main_game.check_fire_collision():
            self.body.insert(0, self.body[0] + self.step)
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, self.body[0] + self.step)
            self.body = body_copy

class Main:
    def __init__(self):
        self.snake = Snake()
        self.fire = Fire()
        self.start_time = pygame.time.get_ticks()
    
    def draw_elements(self):
        self.fire.draw_fire()
        self.snake.draw_snake()

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= 300:
            self.snake.move_snake()
            #self.check_fruit_collision()
            self.check_game_over()
            self.start_time = current_time

    def check_fire_collision(self):
        if self.snake.body[0] == self.fire.pos:
            self.fire.change_location()
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
        image = pygame.transform.scale_by(image, 2)
        image.set_colorkey('black')

        return image
    
pygame.init() # initiates pygame
cell_number = 20
cell_size = 32
FIELD_SIZE = (cell_number * cell_size, cell_number * cell_size)
SCOREBOARD_SIZE = (FIELD_SIZE[1], 30)
WINDOW_SIZE = (FIELD_SIZE[0], FIELD_SIZE[1] + SCOREBOARD_SIZE[1])
window = pygame.display.set_mode(WINDOW_SIZE) # initiates the window
field = pygame.Surface(FIELD_SIZE)

clock = pygame.time.Clock()
pygame.display.set_caption('Snake')

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
    
    field.fill((84, 78, 104))

    main_game.draw_elements()
    window.blit(field, (0,30))

    current_time = main_game.update()

    pygame.display.update()
    clock.tick(60) # window framerate

pygame.quit()