import pygame
import random, sys
from pygame.math import Vector2
from pygame.locals import *
from math import cos
import time

class ParticleSystem:
    def __init__(self):
        self.particle_list = []
        self.start_time = pygame.time.get_ticks()
        self.is_alt_color = False

    def spawn_particles(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= 1500:
            if len(self.particle_list) <= 12:
                self.particle_list.append(Particle(self.is_alt_color))
                if self.is_alt_color:
                    self.is_alt_color = False
                else:
                    self.is_alt_color = True
            self.start_time = current_time

    def draw_particles(self):
        for i, particle in enumerate(self.particle_list):
            if particle.pos[0] <= cell_number * cell_size + particle.glow_circle_radius + 10:
                particle.draw_particle()
            else:
                self.particle_list.pop(i)

class Particle:
    def __init__(self, is_alt_color):
        self.radius = random.randint(1, 2)
        self.x_speed = 0.4
        self.y_speed = 0
        self.x_acceleration = 0
        self.y_acceleration = 0
        self.glow_circle_radius = self.radius * 6
        self.blur_radius = int(self.radius * 5.5)
        self.x_offset = random.randint(0, (cell_number * cell_size)/2)
        self.frec = random.randint(20,100) / 10000
        self.amp = (cell_number * cell_size) / 2.5
        self.is_alt_color = is_alt_color
        x_pos = int(-self.glow_circle_radius * 1.2)
        self.pos = [x_pos, self.trajectory(x_pos)]

    def draw_glow(self):
        color = (90, 50, 40)
        circle_surf = pygame.Surface((self.radius * 30, self.radius * 30))
        pygame.draw.circle(circle_surf, color, (self.radius * 15, self.radius * 15), self.glow_circle_radius)
        circle_surf.set_colorkey('black')
        circle_surf = pygame.transform.gaussian_blur(circle_surf, self.blur_radius)
        field.blit(circle_surf, (self.pos[0] - self.radius * 15, self.pos[1] - self.radius * 15), special_flags=BLEND_RGB_ADD)

    def draw_particle(self):
        color_1 = (255, 170, 94)
        color_2 = (208, 129, 89)
        if not self.is_alt_color:
            pygame.draw.circle(field, color_1, self.pos, self.radius)
        else:
            pygame.draw.circle(field, color_2, self.pos, self.radius)
        self.draw_glow()
        
    def trajectory(self, x_value):
        y_value = cos(x_value * self.frec - self.x_offset) * self.amp + (cell_number * cell_size) / 2
        return y_value

    def move_particle(self):
        self.pos[0] += self.x_speed
        self.pos[1] = self.trajectory(self.pos[0])

class Background:
    def __init__(self):
        self.spritesheet = Spritesheet('assets/background_sprite.png')
    
    def draw_bg(self):
        counter = 2
        for row in range(cell_number):
            for col in range(cell_number):
                if row == 0:
                    frame = self.spritesheet.get_image(16, 16, counter)
                    counter += 1
                    if counter >= 5:
                        counter = 2
                elif col % 2 == 0:
                    frame = self.spritesheet.get_image(16, 16, 0)
                else:
                    frame = self.spritesheet.get_image(16, 16, 1)
                bg_rect = pygame.Rect(col * cell_size, row * cell_size, 32, 32)
                field.blit(frame, bg_rect)

class Fire:
    def __init__(self, body):
        self.glow_radius = 0
        self.change_location(body)
        self.spritesheet = Spritesheet('assets/fire.png')
        self.sprite_list = []
        self.frame_num = 0
        self.load_sprite_list(12)
        self.start_time = pygame.time.get_ticks()
        self.glow_motion = ('center','up','center','down')
        self.motion_counter = 0

    def exclude_randint(self, body):
        vector = Vector2(random.randint(0, cell_number - 1), random.randint(0, cell_number - 1))
        return self.exclude_randint(body) if vector in body else vector
    
    def spawn_animation(self):
        if self.glow_radius <= cell_size // 1.8:
            self.glow_radius += 0.9

    def change_location(self, body):
        self.glow_radius = 0
        self.pos = self.exclude_randint(body)
        self.glow_pos = self.pos

    def load_sprite_list(self, step):
        for i in range(step):
            self.sprite_list.append(self.spritesheet.get_image(16, 16, i))

    def draw_glow(self):
        color = (90, 50, 40)
        circle_surf = pygame.Surface((cell_size * 2, cell_size * 2))
        pygame.draw.circle(circle_surf, color, (cell_size, cell_size), self.glow_radius)
        circle_surf.set_colorkey('black')
        circle_surf = pygame.transform.gaussian_blur(circle_surf, cell_size//2)

        x_coord = self.glow_pos.x * cell_size - cell_size / 2
        y_coord = self.glow_pos.y * cell_size - cell_size / 2
        if self.glow_motion[self.motion_counter] == 'center':
            field.blit(circle_surf, (x_coord, y_coord), special_flags=BLEND_RGB_ADD)
        if self.glow_motion[self.motion_counter] == 'up':
            field.blit(circle_surf, (x_coord, y_coord - 1), special_flags=BLEND_RGB_ADD)
        if self.glow_motion[self.motion_counter] == 'down':
            field.blit(circle_surf, (x_coord, y_coord + 1), special_flags=BLEND_RGB_ADD)

    def draw_fire(self):
        self.spawn_animation()
        fire_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        frame = self.sprite_list[self.frame_num]
        field.blit(frame, fire_rect)
        self.draw_glow()

        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= 150:
            self.motion_counter += 1
            if self.motion_counter >= len(self.glow_motion):
                self.motion_counter = 0
            self.frame_num += 1
            if self.frame_num >= len(self.sprite_list):
                self.frame_num = 0
            self.start_time = current_time
         
class Snake:
    def __init__(self):
        self.body = [Vector2(7,10), Vector2(6,10), Vector2(5,10)]
        self.step = Vector2(1,0)
        self.head = 'right'
        self.spritesheet = Spritesheet('assets/snake_sprite.png')
    
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

class Vignette:
    def __init__(self):
        self.img = pygame.image.load('assets/vignette.png').convert_alpha()
        self.img.set_alpha(125)
        self.img2 = pygame.Surface((SCOREBOARD_SIZE[0], SCOREBOARD_SIZE[1]))
        self.img2.set_alpha(35)

    def draw_vignette_field(self):
        field.blit(self.img, (0,0))

    def draw_vignette_scoreboard(self):
        scoreboard.blit(self.img2, (0,0))

class Main:
    def __init__(self):
        self.snake = Snake()
        self.fire = Fire(self.snake.body)
        self.background = Background()
        self.particle_system = ParticleSystem()
        self.start_time = pygame.time.get_ticks()
        self.collision = False
        self.scoreboard = Scoreboard(SCOREBOARD_SIZE, font)
        self.vignette = Vignette()
        self.pickup_fire_sound = pygame.mixer.Sound('sound/pickup_sfx.wav')
        self.field_music = pygame.mixer.music.load('sound/bg_music.wav')
        pygame.mixer.music.play(-1)

    def draw_elements(self):
        self.scoreboard.draw_scoreboard(len(self.snake.body) - 3)
        self.vignette.draw_vignette_scoreboard()
        self.background.draw_bg()
        self.fire.draw_fire()
        self.snake.draw_snake()
        self.particle_system.draw_particles()
        self.vignette.draw_vignette_field()

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= 100:
            self.collision = self.check_fire_collision()
            self.snake.move_snake()
            self.check_game_over()
            self.start_time = current_time

    def check_fire_collision(self):
        if self.snake.body[0] == self.fire.pos:
            self.pickup_fire_sound.play()
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

class Scoreboard:
    def __init__(self, scoreboard_size, font):
        self.size_x = scoreboard_size[0]
        self.size_y = scoreboard_size[1]
        self.bg = (44, 39, 52)
        self.score_frame = pygame.image.load('assets/score_frame.png')
        self.score_frame_rect = self.score_frame.get_rect()
        self.score_frame_rect.center = (self.size_x / 2, self.size_y / 2)
        self.font = font

    def draw_scoreboard(self, score):
        scoreboard.fill(self.bg)
        scoreboard.blit(self.score_frame, self.score_frame_rect)
        score_render = self.font.render(str(score), True, (255,236,214))
        score_rect = score_render.get_rect()
        score_rect.center = self.score_frame_rect.center
        scoreboard.blit(score_render, score_rect)

pygame.init() # initiates pygame
pygame.mixer.pre_init(44100,-16,2, 512)
cell_number = 15
cell_size = 32
FIELD_SIZE = (cell_number * cell_size, cell_number * cell_size)
SCOREBOARD_SIZE = (FIELD_SIZE[1], 96)
WINDOW_SIZE = (FIELD_SIZE[0], FIELD_SIZE[1] + SCOREBOARD_SIZE[1])
window = pygame.display.set_mode(WINDOW_SIZE) # initiates the window
field = pygame.Surface(FIELD_SIZE)
scoreboard = pygame.Surface(SCOREBOARD_SIZE)
font = pygame.font.Font('font/Retro Gaming.ttf', 25)

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
            if event.key == K_RIGHT or event.key == K_d:
                if previous_direc != l_move:
                    main_game.snake.step = r_move
            if event.key == K_LEFT or event.key == K_a:
                if previous_direc != r_move:
                    main_game.snake.step = l_move
            if event.key == K_UP or event.key == K_w:
                if previous_direc != d_move:
                    main_game.snake.step = u_move
            if event.key == K_DOWN or event.key == K_s:
                if previous_direc != u_move:
                    main_game.snake.step = d_move

    main_game.particle_system.spawn_particles()
    main_game.draw_elements()
    
    for particle in main_game.particle_system.particle_list:
        particle.move_particle()

    window.blit(field, (0, 96))
    window.blit(scoreboard, (0, 0))

    current_time = main_game.update()

    pygame.display.update()
    clock.tick(60) # window framerate

pygame.quit()