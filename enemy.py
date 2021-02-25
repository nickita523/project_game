from pygame import *
from settings import *


class Enemy(sprite.Sprite):
    def __init__(self, pos_x_start, pos_x_end, pos_y_start):
        super().__init__(enemy_group)
        self.change_x = 2
        self.animcount = 0
        self.damage_hero = 0
        self.score = 0
        self.health_enemy = health_enemy
        self.attack_true_r = False
        self.attack_true_l = False
        self.damage_hero = False
        self.hit = False
        self.y = pos_x_start
        self.y1 = pos_x_end
        self.y2 = pos_y_start
        self.pos_x_start = pos_x_start
        self.pos_x_end = pos_x_end
        self.pos_y_start = pos_y_start
        self.x = 0
        self.screen = screen
        self.hit_anim = [
            pygame.image.load('characters\\enemy\\hurt\\0_Golem_Hurt_001.png'),
            pygame.image.load('characters\\enemy\\hurt\\0_Golem_Hurt_002.png'),
            pygame.image.load('characters\\enemy\\hurt\\0_Golem_Hurt_003.png'),
            pygame.image.load('characters\\enemy\\hurt\\0_Golem_Hurt_004.png'),
            pygame.image.load('characters\\enemy\\hurt\\0_Golem_Hurt_005.png'),
            pygame.image.load('characters\\enemy\\hurt\\0_Golem_Hurt_006.png'),
            pygame.image.load('characters\\enemy\\hurt\\0_Golem_Hurt_007.png'),
            pygame.image.load('characters\\enemy\\hurt\\0_Golem_Hurt_008.png'),
            pygame.image.load('characters\\enemy\\hurt\\0_Golem_Hurt_009.png'),
            pygame.image.load('characters\\enemy\\hurt\\0_Golem_Hurt_010.png'),
            pygame.image.load('characters\\enemy\\hurt\\0_Golem_Hurt_011.png')
        ]
        self.walk = [pygame.image.load('characters\\enemy\\walk\\run1.png'),
                     pygame.image.load('characters\\enemy\\walk\\run2.png'),
                     pygame.image.load('characters\\enemy\\walk\\run3.png'),
                     pygame.image.load('characters\\enemy\\walk\\run4.png'),
                     pygame.image.load('characters\\enemy\\walk\\run5.png'),
                     pygame.image.load('characters\\enemy\\walk\\run6.png'),
                     pygame.image.load('characters\\enemy\\walk\\run7.png'),
                     pygame.image.load('characters\\enemy\\walk\\run8.png'),
                     pygame.image.load('characters\\enemy\\walk\\run9.png'),
                     pygame.image.load('characters\\enemy\\walk\\run10.png'),
                     pygame.image.load('characters\\enemy\\walk\\run11.png'),
                     pygame.image.load('characters\\enemy\\walk\\run12.png')]
        self.die_anim = [[pygame.image.load(
            'characters\\enemy\\dying\\0_Golem_Dying_000.png'), 0],
            [pygame.image.load(
                'characters\\enemy\\dying\\0_Golem_Dying_001.png'), 0],
            [pygame.image.load(
                'characters\\enemy\\dying\\0_Golem_Dying_002.png'), 0],
            [pygame.image.load(
                'characters\\enemy\\dying\\0_Golem_Dying_003.png'), 0],
            [pygame.image.load(
                'characters\\enemy\\dying\\0_Golem_Dying_004.png'), 0],
            [pygame.image.load(
                'characters\\enemy\\dying\\0_Golem_Dying_005.png'), 0],
            [pygame.image.load(
                'characters\\enemy\\dying\\0_Golem_Dying_006.png'), 0],
            [pygame.image.load(
                'characters\\enemy\\dying\\0_Golem_Dying_007.png'), 22],
            [pygame.image.load(
                'characters\\enemy\\dying\\0_Golem_Dying_008.png'), 42],
            [pygame.image.load(
                'characters\\enemy\\dying\\0_Golem_Dying_009.png'), 50],
            [pygame.image.load(
                'characters\\enemy\\dying\\0_Golem_Dying_010.png'), 50],
            [pygame.image.load(
                'characters\\enemy\\dying\\0_Golem_Dying_011.png'), 50],
            [pygame.image.load(
                'characters\\enemy\\dying\\0_Golem_Dying_012.png'), 50],
            [pygame.image.load(
                'characters\\enemy\\dying\\0_Golem_Dying_013.png'), 50],
            [pygame.image.load(
                'characters\\enemy\\dying\\0_Golem_Dying_014.png'), 50]]
        self.attack = [[pygame.image.load(
            'characters\\enemy\\attack\\0_Golem_Slashing_000.png'), 0],
            [pygame.image.load(
                'characters\\enemy\\attack\\0_Golem_Slashing_001.png'), 0],
            [pygame.image.load(
                'characters\\enemy\\attack\\0_Golem_Slashing_002.png'), 0],
            [pygame.image.load(
                'characters\\enemy\\attack\\0_Golem_Slashing_003.png'), 50],
            [pygame.image.load(
                'characters\\enemy\\attack\\0_Golem_Slashing_004.png'), 50],
            [pygame.image.load(
                'characters\\enemy\\attack\\0_Golem_Slashing_005.png'), 50],
            [pygame.image.load(
                'characters\\enemy\\attack\\0_Golem_Slashing_006.png'), 50],
            [pygame.image.load(
                'characters\\enemy\\attack\\0_Golem_Slashing_007.png'), 50],
            [pygame.image.load(
                'characters\\enemy\\attack\\0_Golem_Slashing_008.png'), 50],
            [pygame.image.load(
                'characters\\enemy\\attack\\0_Golem_Slashing_009.png'), 50],
            [pygame.image.load(
                'characters\\enemy\\attack\\0_Golem_Slashing_010.png'), 50],
            [pygame.image.load(
                'characters\\enemy\\attack\\0_Golem_Slashing_011.png'), 50]]
        self.rect = Rect(pos_x_start, pos_y_start - 61,
                         enemy_width, enemy_height)
        self.image = pygame.image.load('characters\\enemy\\walk\\run1.png')

    def update(self, camera, player):
        if not self.health_enemy <= 0:
            self.move()
            if not self.attack_true_l and not self.attack_true_r and\
                    not self.hit:
                self.x += self.change_x
            self.check_collision(player)
            self.check_damage(player)
            self.animation()
        else:
            self.die()
        self.rect.x = self.y + self.x - camera.offset.x
        self.rect.y = self.y2 - camera.offset.y - 64
        self.pos_x_start = self.y - camera.offset.x
        self.pos_x_end = self.y1 - camera.offset.x
        self.pos_y_start = self.y2 - camera.offset.y

    def move(self):
        if self.rect.x <= self.pos_x_start:
            self.change_x = 2
        elif self.rect.x + enemy_width >= self.pos_x_end:
            self.change_x = -2

    def animation(self):
        if self.animcount + 1 >= 30:
            self.animcount = 0
            self.hit = False
            self.attack_true_r = False
            self.attack_true_l = False
        if self.hit:
            if self.attack_true_r:
                self.screen.blit(
                    self.hit_anim[int(self.animcount // (30 / 11))],
                    (self.rect.x, self.rect.y))
            else:
                self.screen.blit(pygame.transform.flip(
                    self.hit_anim[int(self.animcount // (30 / 11))], True,
                    False),
                    (self.rect.x, self.rect.y))
        elif self.attack_true_r or self.attack_true_l:
            if self.attack_true_r:
                self.screen.blit(self.attack[int(self.animcount // 2.5)][0],
                                 (self.rect.x, self.rect.y))
            else:
                self.screen.blit(
                    pygame.transform.flip(
                        self.attack[int(self.animcount // 2.5)][0],
                        True, False),
                    (self.rect.x - self.attack[int(self.animcount // 2.5)][1],
                     self.rect.y))
            if self.animcount / 2.5 == 6:
                self.damage_hero = 1
        elif self.change_x > 0:
            self.screen.blit(self.walk[int(self.animcount // 2.5)],
                             (self.rect.x, self.rect.y))
        else:
            self.screen.blit(
                pygame.transform.flip(self.walk[int(self.animcount // 2.5)],
                                      True, False),
                (self.rect.x, self.rect.y))
        self.animcount += 1

    def check_collision(self, player):
        if player.get_player_rect().colliderect(self.rect):
            if self.rect.x + 40 >= player.get_player_rect().x + 82 >= self.rect.x:
                self.attack_true_l = True
            else:
                self.attack_true_r = True

    def check_damage(self, player):
        if player.rect_spear.colliderect(self.rect):
            if player.where_move['attack'] and player.animCount == 27:
                self.hit = True
                self.animcount = 0
                self.health_enemy -= 1

    def die(self, ):
        if self.animcount + 1 >= 30:
            self.animcount = 0
        self.screen.blit(self.die_anim[int(self.animcount // 2)][0],
                         (self.rect.x,
                          self.rect.y + self.die_anim[int(self.animcount // 2)][
                              1]))
        self.animcount += 1
