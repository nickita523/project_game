from pygame import *
from settings import *

current_camera_offset = camera_offset


class Player(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        self.screen = screen
        self.speed = speed
        self.wait_next = 0
        self.change_x = 0
        self.change_y = 0
        self.time_boost = 0
        self.time_jump = 10
        self.animCount = 0
        self.gravitation = 0
        self.score = 0
        self.health = health_player
        self.start_position_x = start_position_x
        self.start_position_y = start_position_y
        self.x = start_position_x
        self.y = start_position_y
        self.hit_tiles = []
        self.rect_spear = Rect(self.x + width_player + 60, self.y, 35,
                               height_player)
        self.hit_anim = [pygame.image.load(
            'characters\\player\\hurt\\Knight_01__HURT_000.png'),
            pygame.image.load(
                'characters\\player\\hurt\\Knight_01__HURT_001.png'),
            pygame.image.load(
                'characters\\player\\hurt\\Knight_01__HURT_002.png'),
            pygame.image.load(
                'characters\\player\\hurt\\Knight_01__HURT_003.png'),
            pygame.image.load(
                'characters\\player\\hurt\\Knight_01__HURT_004.png'),
            pygame.image.load(
                'characters\\player\\hurt\\Knight_01__HURT_005.png'),
            pygame.image.load(
                'characters\\player\\hurt\\Knight_01__HURT_006.png'),
            pygame.image.load(
                'characters\\player\\hurt\\Knight_01__HURT_007.png'),
            pygame.image.load(
                'characters\\player\\hurt\\Knight_01__HURT_008.png'),
            pygame.image.load(
                'characters\\player\\hurt\\Knight_01__HURT_009.png')]
        self.attack_anim = [
            [pygame.image.load('characters\\player\\attack\\attack1.png'), 107],
            [pygame.image.load('characters\\player\\attack\\attack2.png'), 105],
            [pygame.image.load('characters\\player\\attack\\attack3.png'), 95],
            [pygame.image.load('characters\\player\\attack\\attack4.png'), 89],
            [pygame.image.load('characters\\player\\attack\\attack5.png'), 80],
            [pygame.image.load('characters\\player\\attack\\attack6.png'), 73],
            [pygame.image.load('characters\\player\\attack\\attack7.png'), 71],
            [pygame.image.load('characters\\player\\attack\\attack8.png'), 81],
            [pygame.image.load('characters\\player\\attack\\attack9.png'), 95],
            [pygame.image.load('characters\\player\\attack\\attack10.png'), 100]
        ]
        self.where_move = {'Left': False, 'Right': False, 'Jump': False,
                           'Down': False, 'Up': False, 'Stay_Right': False,
                           'Collision_Bottom': False, 'die': False,
                           'attack': False, 'hit': False}
        self.playerStand = pygame.image.load('characters\\player\\stay.png')
        self.walk_anim = [
            pygame.image.load('characters\\player\\walk\\Walk1.png'),
            pygame.image.load('characters\\player\\walk\\Walk2.png'),
            pygame.image.load('characters\\player\\walk\\Walk3.png'),
            pygame.image.load('characters\\player\\walk\\Walk4.png'),
            pygame.image.load('characters\\player\\walk\\Walk4.png'),
            pygame.image.load('characters\\player\\walk\\Walk6.png'),
            pygame.image.load('characters\\player\\walk\\Walk7.png'),
            pygame.image.load('characters\\player\\walk\\Walk8.png'),
            pygame.image.load('characters\\player\\walk\\Walk9.png'),
            pygame.image.load('characters\\player\\walk\\Walk10.png')]
        self.jump_anim = [
            pygame.image.load('characters\\player\\jump\\jump1.png'),
            pygame.image.load('characters\\player\\jump\\jump2.png'),
            pygame.image.load('characters\\player\\jump\\jump3.png'),
            pygame.image.load('characters\\player\\jump\\jump9.png'),
            pygame.image.load('characters\\player\\jump\\jump9.png'),
            pygame.image.load('characters\\player\\jump\\jump10.png')]
        self.death = [[pygame.image.load(
            'characters\\player\\death\\Knight_01__DIE_000.png'), 0],
            [pygame.image.load(
                'characters\\player\\death\\Knight_01__DIE_001.png'),
                0],
            [pygame.image.load(
                'characters\\player\\death\\Knight_01__DIE_002.png'),
                0],
            [pygame.image.load(
                'characters\\player\\death\\Knight_01__DIE_003.png'),
                0],
            [pygame.image.load(
                'characters\\player\\death\\Knight_01__DIE_004.png'),
                0],
            [pygame.image.load(
                'characters\\player\\death\\Knight_01__DIE_005.png'),
                65],
            [pygame.image.load(
                'characters\\player\\death\\Knight_01__DIE_006.png'),
                65],
            [pygame.image.load(
                'characters\\player\\death\\Knight_01__DIE_007.png'),
                65],
            [pygame.image.load(
                'characters\\player\\death\\Knight_01__DIE_008.png'),
                65],
            [pygame.image.load(
                'characters\\player\\death\\Knight_01__DIE_009.png'),
                65], ]
        self.player_fall = pygame.image.load(
            'characters\\player\\jump\\jump3.png')

    def update(self, damage):
        self.rect = self.get_player_rect()
        self.move_key()
        self.move()
        if self.health <= 0:
            self.where_move['die'] = True
            self.start_die()
        elif self.where_move['attack'] and self.where_move['Collision_Bottom'] \
                and not self.where_move['hit']:
            player_rect = self.get_player_rect()
            self.health -= damage
            for i in enemy_group:
                i.damage_hero = 0
            if self.where_move['Stay_Right']:
                self.rect_spear = Rect(player_rect.x + width_player + 60,
                                       player_rect.y, 35,
                                       height_player)
            else:
                self.rect_spear = Rect(player_rect.x - 80,
                                       player_rect.y, 35,
                                       height_player)
            self.animation()
        else:
            self.x += self.change_x
            self.collision_test()
            for tile in self.hit_tiles:
                if self.change_x > 0:
                    self.rect.right = tile.rect.left
                    self.x = self.rect.x + current_camera_offset.x
                elif self.change_x < 0:
                    self.rect.left = tile.rect.right
                    self.x = self.rect.x + current_camera_offset.x
            if self.where_move['Up']:
                self.jump()
            if not self.where_move['Collision_Bottom'] and \
                    self.gravitation < 50 and not self.where_move['Up']:
                self.gravitation += 1
            self.where_move['Collision_Bottom'] = False
            self.y += self.gravitation + self.change_y
            self.collision_test()
            for tile in self.hit_tiles:
                if self.change_y < 0:
                    self.rect.top = tile.rect.bottom
                    self.y = self.rect.y + current_camera_offset.y
                elif self.change_y > 0 or self.gravitation != 0:
                    self.rect.bottom = tile.rect.top
                    self.y = self.rect.y + current_camera_offset.y
                    self.where_move['Up'] = False
                    self.time_jump = 10
                    self.where_move['Collision_Bottom'] = True
                    self.gravitation = 0
            if damage != 0:
                self.health -= damage
                for i in enemy_group:
                    i.damage_hero = 0
                self.where_move['hit'] = True
            self.boost_check()
            self.rect = self.get_player_rect()
            self.animation()

    def move_key(self):
        get_pressed = pygame.key.get_pressed()
        if get_pressed[pygame.K_a]:
            self.where_move['Left'] = True
            self.where_move['Right'] = False
            self.where_move['Stay_Right'] = False
        elif get_pressed[pygame.K_d]:
            self.where_move['Right'] = True
            self.where_move['Left'] = False
            self.where_move['Stay_Right'] = True
        else:
            self.where_move['Right'] = False
            self.where_move['Left'] = False
        if get_pressed[pygame.K_w] and not self.where_move['Up'] and \
                self.where_move['Collision_Bottom']:
            self.where_move['Up'] = True
            self.animCount = 0
        if get_pressed[pygame.K_q] and not self.where_move['die'] and \
                self.wait_next >= 30:
            self.wait_next = 0
            self.animCount = 0
            self.where_move['attack'] = True
        self.wait_next += 1

    def move(self):
        if self.where_move['Right']:
            self.change_x = self.speed
        elif self.where_move['Left']:
            self.change_x = -self.speed
        else:
            self.change_x = 0

    def jump(self):
        if self.time_jump >= -10:
            self.change_y = -(self.time_jump ** 2) * 0.5
            if self.time_jump < 0:
                self.change_y = (self.time_jump ** 2) * 0.5
            self.time_jump -= 1
        else:
            self.change_y = 0
            self.time_jump = 10
            self.where_move['Up'] = False

    def animation(self):
        if self.animCount + 1 >= 30:
            self.animCount = 0
            self.where_move['attack'] = False
        if self.animCount >= 25:
            self.where_move['hit'] = False
        if self.where_move['hit']:
            if self.where_move['Stay_Right']:
                self.screen.blit(
                    self.hit_anim[int(self.animCount // 2.5)],
                    (self.rect.x, self.rect.y))
            else:
                self.screen.blit(
                    pygame.transform.flip(
                        self.hit_anim[int(self.animCount // 2.5)],
                        True, False),
                    (self.rect.x - width_player, self.rect.y))
            self.animCount += 1
        elif self.where_move['attack']:
            if self.where_move['Stay_Right']:
                self.screen.blit(
                    self.attack_anim[self.animCount // 3][0],
                    (self.rect.x, self.rect.y))
            else:
                self.screen.blit(
                    pygame.transform.flip(
                        self.attack_anim[self.animCount // 3][0],
                        True, False),
                    (self.rect.x - self.attack_anim[self.animCount // 3][1],
                     self.rect.y))
            self.animCount += 1
        elif self.where_move['Up']:
            if self.where_move['Stay_Right']:
                self.screen.blit(
                    self.jump_anim[self.animCount // 5],
                    (self.rect.x, self.rect.y))
                self.animCount += 1
            else:
                self.screen.blit(
                    pygame.transform.flip(self.jump_anim[self.animCount // 5],
                                          True, False),
                    (self.rect.x - width_player, self.rect.y))
                self.animCount += 1
        elif self.gravitation > 1:
            if self.where_move['Stay_Right']:
                self.screen.blit(
                    self.player_fall,
                    (self.rect.x, self.rect.y))
                self.animCount = 0
            else:
                self.screen.blit(
                    pygame.transform.flip(self.player_fall, True, False),
                    (self.rect.x - width_player, self.rect.y))
                self.animCount = 0
        elif self.where_move['Right']:
            self.screen.blit(
                self.walk_anim[self.animCount // 3],
                (self.rect.x, self.rect.y))
            self.animCount += 1
        elif self.where_move['Left']:
            self.screen.blit(
                pygame.transform.flip(self.walk_anim[self.animCount // 3], True,
                                      False),
                (self.rect.x - width_player, self.rect.y))
            self.animCount += 1
        elif not self.where_move['Right'] and not self.where_move['Left']:
            if self.where_move['Stay_Right']:
                self.screen.blit(
                    self.playerStand,
                    (self.rect.x, self.rect.y))
                self.animCount = 0
            else:
                self.screen.blit(
                    pygame.transform.flip(self.playerStand, True, False),
                    (self.rect.x - width_player, self.rect.y))
                self.animCount = 0

    def collision_test(self):
        self.hit_tiles = []
        self.rect = self.get_player_rect()
        for tile in tiles_group:
            if self.rect.colliderect(tile):
                self.hit_tiles.append(tile)
        for spike in spike_group:
            if self.rect.colliderect(spike):
                self.health = 0

    def start_die(self):
        if self.animCount + 1 >= 30:
            self.animCount = 0
            self.x = self.start_position_x
            self.y = self.start_position_y
            self.health = health_player
            self.where_move['die'] = False
            for i in enemy_group:
                i.damage_hero = 0
        player_rect = self.get_player_rect()
        self.rect_spear = Rect(player_rect.x + width_player + 60, player_rect.y,
                               35, height_player)
        self.screen.blit(self.death[self.animCount // 3][0],
                         (player_rect.x,
                          player_rect.y + self.death[self.animCount // 3][1]))
        self.animCount += 1

    def check_level(self):
        player_rect = self.get_player_rect()
        for flag in flag_group:
            if player_rect.colliderect(flag):
                return True

    def boost_check(self):
        player_rect = self.get_player_rect()
        for health in health_group:
            if player_rect.colliderect(health) and self.health != health_player:
                self.health += 1
                remove_objects.append((health.pos_x / 64, health.pos_y / 64))
        for boost in speed_group:
            if player_rect.colliderect(boost):
                self.speed = speed + 3
                remove_objects.append((boost.pos_x / 64, boost.pos_y / 64))
                self.time_boost = 90
        for crystal in crystal_group:
            if player_rect.colliderect(crystal):
                self.score += 1000
                remove_objects.append((crystal.pos_x / 64, crystal.pos_y / 64))
                self.time_boost = 60
        for teleport in teleport_group:
            if player_rect.colliderect(teleport):
                self.x = teleport.where_x
                self.y = teleport.where_y
        if self.time_boost != 0:
            self.time_boost -= 1
        else:
            self.speed = speed

    def get_player_rect(self):
        return Rect(self.x - current_camera_offset.x,
                    self.y - current_camera_offset.y,
                    width_player,
                    height_player)

    def player_start(self, pos_x, pos_y):
        self.start_position_x = pos_x
        self.start_position_y = pos_y
        self.x = pos_x
        self.y = pos_y
