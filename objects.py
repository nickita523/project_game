from settings import *


class Teleport(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, where_x, where_y, anim_count):
        super().__init__(teleport_group)
        self.pos_x = pos_x
        self.pos_y = pos_y - 64
        self.where_x = where_x
        self.where_y = where_y
        self.image = tiles['K'][int(anim_count / 7.5)]
        self.rect = pygame.Rect(pos_x, pos_y, 52, 125)

    def update(self, camera):
        self.rect = pygame.Rect(self.rect.x - camera.offset.x,
                                self.rect.y - camera.offset.y,
                                52, 125)
        self.where_x = self.where_x
        self.where_y = self.where_y


class BeautifulTiles(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, sym):
        super().__init__(beautiful_group)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = tiles[sym][0]
        self.rect = pygame.Rect(pos_x, pos_y - tiles[sym][1], 64, 64)

    def update(self, camera):
        self.rect = pygame.Rect(self.rect.x - camera.offset.x,
                                self.rect.y - camera.offset.y,
                                64, 64)


class Crystal(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, anim_count, player):
        super().__init__(crystal_group)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = tiles['C'][anim_count // 3]
        self.rect = pygame.Rect(pos_x, pos_y, 64, 64)
        self.player = player

    def update(self, camera):
        self.rect = pygame.Rect(self.rect.x - camera.offset.x,
                                self.rect.y - camera.offset.y,
                                64, 64)


class SpeedBoost(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, anim_count, player):
        super().__init__(speed_group)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = tiles['B'][int(anim_count // (30 / 16))]
        self.rect = pygame.Rect(pos_x, pos_y, 64, 64)
        self.player = player

    def update(self, camera):
        self.rect = pygame.Rect(self.rect.x - camera.offset.x,
                                self.rect.y - camera.offset.y,
                                64, 64)


class HealthBoost(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, anim_count, player):
        super().__init__(health_group)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = tiles['H'][int(anim_count // 7.5)]
        self.rect = pygame.Rect(pos_x, pos_y, 64, 64)
        self.player = player

    def update(self, camera):
        self.rect = pygame.Rect(self.rect.x - camera.offset.x,
                                self.rect.y - camera.offset.y,
                                64, 64)


class Spike(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(spike_group)
        self.image = tiles['S']
        self.rect = pygame.Rect(pos_x, pos_y + 44, 64, 21)

    def update(self, camera):
        self.rect = pygame.Rect(self.rect.x - camera.offset.x,
                                self.rect.y - camera.offset.y,
                                64, 21)


class Flag(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, anim_count):
        super().__init__(flag_group)
        self.image = tiles['F'][int(anim_count // 7.5)]
        self.rect = pygame.Rect(pos_x, pos_y - 64, 64, 64)

    def update(self, camera):
        self.rect = pygame.Rect(self.rect.x - camera.offset.x,
                                self.rect.y - camera.offset.y, 64,
                                64)


class Tile(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y):
        super().__init__(tiles_group)
        if image in tiles:
            self.image = tiles[image]
        else:
            self.image = image
        self.rect = pygame.Rect(pos_x, pos_y, 64, 64)

    def update(self, camera):
        self.rect = pygame.Rect(self.rect.x - camera.offset.x,
                                self.rect.y - camera.offset.y, 64,
                                64)


class CoinCreate(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y):
        super().__init__(objects_group)
        self.image = pygame.image.load('objects\\coin\\coin0.png')
        self.rect = pygame.Rect(pos_x, pos_y, 32, 32)
        self.pos_x = pos_x
        self.pos_y = pos_y

    def update(self, camera):
        self.rect = pygame.Rect(self.rect.x - camera.offset.x,
                                self.rect.y - camera.offset.y, 32,
                                32)
