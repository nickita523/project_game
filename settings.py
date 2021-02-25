import pygame

window_size = (1920, 1080)
bar_length = 200
bar_height = 20
width_player = 85
height_player = 125
enemy_width = 82
enemy_height = 125
start_position_x = 115
start_position_y = 500
health_player = 10
health_enemy = 2
speed = 7
remove_objects = []
teleport_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
objects_group = pygame.sprite.Group()
flag_group = pygame.sprite.Group()
spike_group = pygame.sprite.Group()
health_group = pygame.sprite.Group()
speed_group = pygame.sprite.Group()
crystal_group = pygame.sprite.Group()
beautiful_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
screen = pygame.display.set_mode(window_size, 0, 0)
tiles = {'D': pygame.image.load('tiles\\Tile_D.png'),
         'G': pygame.image.load('tiles\\Tile_G.png'),
         'S': pygame.image.load('tiles\\Tile_S.png'),
         'L': pygame.image.load('tiles\\Tile_L.png'),
         'R': pygame.image.load('tiles\\Tile_R.png'),
         'l': pygame.image.load('tiles\\Tile_left.png'),
         'r': pygame.image.load('tiles\\Tile_right.png'),
         '1': (pygame.image.load('tiles\\tree1.png'), 320),
         '2': (pygame.image.load('tiles\\tree2.png'), 400),
         '3': (pygame.image.load('tiles\\tree3.png'), 300),
         '4': (pygame.image.load('tiles\\bushes1.png'), 20),
         '5': (pygame.image.load('tiles\\bushes2.png'), 5),
         '6': (pygame.image.load('tiles\\bushes3.png'), 15),
         '[': (pygame.image.load('tiles\\Tile_[.png')),
         ']': (pygame.image.load('tiles\\Tile_].png')),
         '{': (pygame.image.load('tiles\\Tile_{.png')),
         '}': (pygame.image.load('tiles\\Tile_}.png')),
         '=': (pygame.image.load('tiles\\Tile_=.png')),
         'Q': (pygame.image.load('tiles\\Tile_Q.png')),
         'q': (pygame.image.load('tiles\\Tile_Conner_q.png')),
         'Z': (pygame.image.load('tiles\\Tile_Z.png')),
         'I': (pygame.image.load('tiles\\Tile_I.png')),
         'O': (pygame.image.load('tiles\\Tile_O.png')),
         'F': [pygame.image.load('objects\\flag\\flag0.png'),
               pygame.image.load('objects\\flag\\flag1.png'),
               pygame.image.load('objects\\flag\\flag2.png'),
               pygame.image.load('objects\\flag\\flag3.png')],
         'H': [pygame.image.load('objects\\health\\heart1.png'),
               pygame.image.load('objects\\health\\heart2.png'),
               pygame.image.load('objects\\health\\heart3.png'),
               pygame.image.load('objects\\health\\heart4.png'),
               pygame.image.load('objects\\health\\heart5.png'),
               pygame.image.load('objects\\health\\heart6.png'),
               pygame.image.load('objects\\health\\heart7.png'),
               pygame.image.load('objects\\health\\heart8.png'),
               pygame.image.load('objects\\health\\heart9.png'),
               pygame.image.load('objects\\health\\heart10.png')],
         'B': [pygame.image.load('objects\\speed\\speed1.png'),
               pygame.image.load('objects\\speed\\speed2.png'),
               pygame.image.load('objects\\speed\\speed3.png'),
               pygame.image.load('objects\\speed\\speed4.png'),
               pygame.image.load('objects\\speed\\speed5.png'),
               pygame.image.load('objects\\speed\\speed6.png'),
               pygame.image.load('objects\\speed\\speed7.png'),
               pygame.image.load('objects\\speed\\speed8.png'),
               pygame.image.load('objects\\speed\\speed9.png'),
               pygame.image.load('objects\\speed\\speed10.png'),
               pygame.image.load('objects\\speed\\speed11.png'),
               pygame.image.load('objects\\speed\\speed12.png'),
               pygame.image.load('objects\\speed\\speed13.png'),
               pygame.image.load('objects\\speed\\speed14.png'),
               pygame.image.load('objects\\speed\\speed15.png'),
               pygame.image.load('objects\\speed\\speed16.png')],
         'C': [pygame.image.load('objects\\crystal\\crystal1.png'),
               pygame.image.load('objects\\crystal\\crystal2.png'),
               pygame.image.load('objects\\crystal\\crystal3.png'),
               pygame.image.load('objects\\crystal\\crystal4.png'),
               pygame.image.load('objects\\crystal\\crystal5.png'),
               pygame.image.load('objects\\crystal\\crystal6.png'),
               pygame.image.load('objects\\crystal\\crystal7.png'),
               pygame.image.load('objects\\crystal\\crystal8.png'),
               pygame.image.load('objects\\crystal\\crystal9.png'),
               pygame.image.load('objects\\crystal\\crystal10.png')],
         'K': [pygame.image.load('objects\\teleport\\sprite_0.png'),
               pygame.image.load('objects\\teleport\\sprite_1.png'),
               pygame.image.load('objects\\teleport\\sprite_2.png'),
               pygame.image.load('objects\\teleport\\sprite_3.png')]}
vec = pygame.math.Vector2
camera_offset = vec(0, 0)
