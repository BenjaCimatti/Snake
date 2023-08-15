import pygame
import random, sys
from pygame.math import Vector2
from pygame.locals import *
from math import sin, cos

class ParticleSystem:
    def __init__(self):
        self.particle_list = []
        self.start_time = pygame.time.get_ticks()

    def spawn_particles(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= 1500:
            self.particle_list.append(Particle())
            self.start_time = current_time

    def draw_particles(self):
        for i, particle in enumerate(self.particle_list):
            if particle.pos[0] <= cell_number * cell_size + particle.radius:
                particle.draw_particle()
            else:
                self.particle_list.pop(i)

class Particle:
    def __init__(self):
        self.pos = [0, random.randint(0, cell_number * cell_size)]
        self.radius = random.randint(1, 2)
        self.x_speed = random.randint(3,6) / 10
        self.y_speed = 0
        self.x_acceleration = 0
        self.y_acceleration = 0
        self.glow_circle_radius = self.radius * 10
        self.blur_radius = self.radius * 4

    def draw_glow(self):
        color = (90, 50, 40)
        circle_surf = pygame.Surface((self.radius * 30, self.radius * 30))
        pygame.draw.circle(circle_surf, color, (self.radius * 15, self.radius * 15), self.glow_circle_radius)
        circle_surf.set_colorkey('black')
        circle_surf = pygame.transform.gaussian_blur(circle_surf, self.blur_radius)
        field.blit(circle_surf, (self.pos[0] - self.radius * 15, self.pos[1] - self.radius * 15), special_flags=BLEND_RGB_ADD)

    def draw_particle(self):
        color = (255, 170, 94)
        pygame.draw.circle(field, color, self.pos, self.radius)
        self.draw_glow()
        

    def move_particle(self):
        frec_multiplier = random.randint(1, 5) / 100 # 0.01 to 0.05
        amp_multiplier = random.randint(5, 10) / 10 # 0.5 to 1
        self.pos[0] += self.x_speed
        self.pos[1] += sin(self.pos[0] * frec_multiplier) * amp_multiplier

class Background:
    def __init__(self):
        self.spritesheet = Spritesheet('assets/background_sprite.png')
    
    def draw_bg(self):
        for row in range(cell_number):
            for col in range(cell_number):
                if col % 2 == 0:
                    frame = self.spritesheet.get_image(16, 16, 0)
                else:
                    frame = self.spritesheet.get_image(16, 16, 1)
                bg_rect = pygame.Rect(col * cell_size, row * cell_size, 16, 16)
                field.blit(frame, bg_rect)

class Fire:
    def __init__(self, body):
        self.change_location(body)
        self.spritesheet = Spritesheet('assets/fire.png')
        self.sprite_list = []
        self.frame = 0
        self.load_sprite_list(12)
        self.start_time = pygame.time.get_ticks()
        self.glow_motion = ('center','up','center','down')
        self.motion_counter = -1

    def exclude_randint(self, body):
        vector = Vector2(random.randint(0, cell_number - 1), random.randint(0, cell_number - 1))
        return self.exclude_randint(body) if vector in body else vector

    def change_location(self, body):
        self.pos = self.exclude_randint(body)
        self.glow_pos = self.pos

    def load_sprite_list(self, step):
        for i in range(step):
            self.sprite_list.append(self.spritesheet.get_image(16, 16, i))

    def draw_glow(self):
        color = (90, 50, 40)
        circle_surf = pygame.Surface((cell_size * 2, cell_size * 2))
        pygame.draw.circle(circle_surf, color, (cell_size, cell_size), cell_size//1.8)
        circle_surf.set_colorkey('black')
        circle_surf = pygame.transform.gaussian_blur(circle_surf, cell_size//2)

        x_coord = self.glow_pos.x * cell_size - cell_size / 2
        y_coord = self.glow_pos.y * cell_size - cell_size / 2
        if self.glow_motion[self.motion_counter] == 'center':
            field.blit(circle_surf, (x_coord, y_coord), special_flags=BLEND_RGB_ADD)
        if self.glow_motion[self.motion_counter] == 'up':
            field.blit(circle_surf, (x_coord - 1, y_coord - 1), special_flags=BLEND_RGB_ADD)
        if self.glow_motion[self.motion_counter] == 'down':
            field.blit(circle_surf, (x_coord + 1, y_coord + 1), special_flags=BLEND_RGB_ADD)

    def draw_fire(self):
        fire_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)

        field.blit(self.sprite_list[self.frame], fire_rect)
        self.draw_glow()

        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= 150:
            self.motion_counter += 1
            if self.motion_counter >= len(self.glow_motion):
                self.motion_counter = 0
            self.frame += 1
            if self.frame >= len(self.sprite_list):
                self.frame = 0
            self.start_time = current_time
         
class Snake:
    def __init__(self):
        self.body = [Vector2(7,10), Vector2(6,10), Vector2(5,10)]
        self.step = Vector2(1,0)
        self.head = 'right'
        self.spritesheet = Spritesheet('assets/snake_sprite_alt.png')
    
    def draw_snake(self):
        self.update_head()
        for index, block in enumerate(self.body):
            block_rect = pygame.Rect(int(block.x * cell_size), int(block.y * cell_size), cell_size, cell_size)
            prev_block = self.body[index-1]

            if index == 0:
                if self.head == 'right':
                    field.blit(self.spritesheet.get_image(16, 16, 1), block_rect)
                elif self.head == 'left':
                    field.blit(self.spritesheet.get_image(16, 16, 3), block_rect)
                elif self.head == 'up':
                    field.blit(self.spritesheet.get_image(16, 16, 0), block_rect)
                elif self.head == 'down':
                    field.blit(self.spritesheet.get_image(16, 16, 2), block_rect)

            elif index == len(self.body) - 1:
                if prev_block.x > block.x:
                    field.blit(self.spritesheet.get_image(16, 16, 7), block_rect)
                elif prev_block.x < block.x:
                    field.blit(self.spritesheet.get_image(16, 16, 9), block_rect)
                elif prev_block.y > block.y:
                    field.blit(self.spritesheet.get_image(16, 16, 8), block_rect)
                elif prev_block.y < block.y:
                    field.blit(self.spritesheet.get_image(16, 16, 6), block_rect)
            
            else:
                next_block = self.body[index+1]

                if (prev_block.x < block.x and next_block.y > block.y) or (next_block.x < block.x and prev_block.y > block.y):
                    field.blit(self.spritesheet.get_image(16, 16, 10), block_rect)
                if (prev_block.x < block.x and next_block.y < block.y) or (next_block.x < block.x and prev_block.y < block.y):
                    field.blit(self.spritesheet.get_image(16, 16, 11), block_rect)
                if (prev_block.x > block.x and next_block.y < block.y) or (next_block.x > block.x and prev_block.y < block.y):
                    field.blit(self.spritesheet.get_image(16, 16, 12), block_rect)
                if (prev_block.x > block.x and next_block.y > block.y) or (next_block.x > block.x and prev_block.y > block.y):
                    field.blit(self.spritesheet.get_image(16, 16, 13), block_rect)

                if prev_block.y == block.y == next_block.y:
                    field.blit(self.spritesheet.get_image(16, 16, 5),block_rect)
                if prev_block.x == block.x == next_block.x:
                    field.blit(self.spritesheet.get_image(16, 16, 4),block_rect)
                
    def update_head(self):
        head_relation = self.body[0] - self.body[1]
        if head_relation == Vector2(1,0): self.head = 'right'
        if head_relation == Vector2(-1,0): self.head = 'left'
        if head_relation == Vector2(0,1): self.head = 'down'
        if head_relation == Vector2(0,-1): self.head = 'up'


    def move_snake(self):
        if main_game.collision:
            self.body.insert(0, self.body[0] + self.step)
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, self.body[0] + self.step)
            self.body = body_copy

class Main:
    def __init__(self):
        self.snake = Snake()
        self.fire = Fire(self.snake.body)
        self.background = Background()
        self.particle_system = ParticleSystem()
        self.start_time = pygame.time.get_ticks()
        self.collision = False
    
    def draw_elements(self):
        self.background.draw_bg()
        self.fire.draw_fire()
        self.snake.draw_snake()
        self.particle_system.draw_particles()

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= 120:
            self.collision = self.check_fire_collision()
            self.snake.move_snake()
            self.check_game_over()
            self.start_time = current_time

    def check_fire_collision(self):
        if self.snake.body[0] == self.fire.pos:
            self.fire.change_location(self.snake.body)
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
cell_number = 15
cell_size = 32
FIELD_SIZE = (cell_number * cell_size, cell_number * cell_size)
SCOREBOARD_SIZE = (FIELD_SIZE[1], 48)
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

    main_game.particle_system.spawn_particles()
    main_game.draw_elements()
    
    for particle in main_game.particle_system.particle_list:
        particle.move_particle()

    window.blit(field, (0, 48))

    current_time = main_game.update()

    pygame.display.update()
    clock.tick(60) # window framerate

pygame.quit()