from player import Player
from enemy import Enemy
from objects import *
from settings import *

enemies = []
all_sprites_mas = [objects_group, tiles_group, flag_group, spike_group,
                   health_group, speed_group, crystal_group, beautiful_group]
boosts_sprites = [health_group, speed_group, spike_group, flag_group,
                  crystal_group]
teleports = [[(7616, 2112), (7488, 1472)]]
all_levels = ['level_1', 'level_2']
current_camera_offset = camera_offset


def main():
    pygame.init()
    start_menu()
    with open('levels\\now.txt', 'r') as f:
        level_num = int(f.read())
    level = load_level('levels\\' + all_levels[level_num - 1] + '.txt')
    total_width = len(level[0]) * 64
    total_height = len(level) * 64
    anim_count = 5
    bg = pygame.image.load('bg.png')
    player = Player()
    coin = Coin()
    running = True
    clock = pygame.time.Clock()
    pos_y_start = 0
    pos_x_start = 0
    pos_x_end = 0
    score_add = 0
    camera = Camera(player, total_width, total_height)
    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.blit(bg, (0, 0))
        for i in all_sprites_mas:
            i.empty()
        teleport_group.empty()
        y = 0
        count = 0
        all_damage = 0
        if remove_objects:
            for i in remove_objects:
                level[int(i[1])][int(i[0])] = '-'
        for line_of_sym in level:
            x = 0
            for sym in line_of_sym:
                if sym != '-':
                    if sym == 'D' or sym == 'G' or sym == 'L' or sym == 'R' or \
                            sym == 'r' or sym == 'l' or sym == '{' or \
                            sym == '}' or sym == '[' or sym == ']' or \
                            sym == 'Q' or sym == 'q' or sym == 'Z' or \
                            sym == '=' or sym == 'I' or sym == 'O':
                        Tile(sym, x * 64, y * 64)
                    elif sym == '1' or sym == '2' or sym == '3' or sym == '4' \
                            or sym == '5' or sym == '6':
                        BeautifulTiles(x * 64, y * 64, sym)
                    elif sym == 'o':
                        CoinCreate(x * 64, y * 64)
                    elif sym == 'F':
                        Flag(x * 64, y * 64, anim_count)
                    elif sym == 'S':
                        Spike(x * 64, y * 64)
                    elif sym == 'H':
                        HealthBoost(x * 64, y * 64, anim_count, player)
                    elif sym == 'B':
                        SpeedBoost(x * 64, y * 64, anim_count, player)
                    elif sym == 'C':
                        Crystal(x * 64, y * 64, anim_count, player)
                    elif sym == 'P':
                        player.player_start(x * 64, y * 64 + 64)
                        remove_objects.append((x, y))
                    if sym == 'E':
                        pos_y_start = y * 64
                        level[y][x] = '-'
                        if count == 0:
                            pos_x_start = x * 64
                        elif level[y][x + 1] != 'E':
                            pos_x_end = x * 64
                        count += 1
                    elif count != 0:
                        enemies.append(
                            Enemy(pos_x_start, pos_x_end, pos_y_start))
                        count = 0
                x += 1
            count = 0
            y += 1
        Teleport(teleports[0][0][0], teleports[0][0][1], teleports[0][1][0],
                 teleports[0][1][1], anim_count)
        if anim_count + 1 >= 30:
            anim_count = 0
        anim_count += 1
        camera.scroll()
        for group in all_sprites_mas:
            group.update(camera)
        for i in enemies:
            all_damage += i.damage_hero
        beautiful_group.draw(screen)
        for i in boosts_sprites:
            i.draw(screen)
        teleport_group.update(camera)
        player.update(all_damage)
        score = coin.update(objects_group, player.get_player_rect(), anim_count)
        score += score_add
        score += player.score
        tiles_group.draw(screen)
        objects_group.draw(screen)
        for i in enemies:
            i.update(camera, player)
            if i.health_enemy <= 0 and i.animcount == 29:
                score_add += 200
                enemies.remove(i)
        if player.where_move['die'] and player.animCount == 29:
            score_add = 0
            coin = Coin()
            enemies.clear()
            remove_objects.clear()
            death_menu(score)
            with open('levels\\now.txt', 'r') as f:
                level_num = int(f.read())
            level = load_level(
                'levels\\' + all_levels[level_num - 1] + '.txt')
        if player.check_level():
            try:
                with open('levels\\what_level.txt', 'w') as f:
                    f.write(str(level_num + 1))
                enemies.clear()
                remove_objects.clear()
                player = Player()
                camera = Camera(player, total_width, total_height)
                coin = Coin()
                score_add = 0
                end_menu(score)
                with open('levels\\now.txt', 'r') as f:
                    level_num = int(f.read())
                level = load_level(
                    'levels\\' + all_levels[level_num - 1] + '.txt')
            except:
                pass
        teleport_group.draw(screen)
        health_bar(player)
        screen_score(score)
        pygame.display.update()
        pygame.display.flip()
    pygame.quit()


class Coin:
    def __init__(self):
        super().__init__()
        self.coin_anim = [pygame.image.load('objects\\coin\\coin0.png'),
                          pygame.image.load('objects\\coin\\coin1.png'),
                          pygame.image.load('objects\\coin\\coin2.png'),
                          pygame.image.load('objects\\coin\\coin3.png'),
                          pygame.image.load('objects\\coin\\coin4.png'),
                          pygame.image.load('objects\\coin\\coin5.png')]
        self.screen = screen
        self.animCount = 0
        self.point = 0
        self.coins_rect = []
        self.player = pygame.Rect(0, 0, 0, 0)

    def update(self, coins_rect, player, animcount):
        self.animCount = animcount
        self.coins_rect = coins_rect
        self.player = player
        self.animation()
        self.check_rect()
        return self.point

    def check_rect(self):
        for coin in objects_group:
            if self.player.colliderect(coin):
                self.point += 100
                remove_objects.append((coin.pos_x / 64, coin.pos_y / 64))

    def animation(self):
        for i in objects_group:
            i.image = self.coin_anim[self.animCount // 5]


class Camera:
    def __init__(self, player, width, height):
        vec = pygame.math.Vector2
        self.player = player
        self.offset = vec(0, 0)
        self.offset_float = vec(0, 0)
        self.DISPLAY_W, self.DISPLAY_H = 1920, 1080
        self.CONST = vec(-self.DISPLAY_W / 2, -self.DISPLAY_H / 2)
        self.total_w = width
        self.total_h = height
        self.player = player

    def scroll(self):
        self.offset_float.x += (
                self.player.x - self.offset_float.x +
                self.CONST.x)
        self.offset.x = max(0, min(int(self.offset_float.x),
                                   self.total_w - self.DISPLAY_W))
        self.offset.x = max(0, min(int(self.offset_float.x),
                                   self.total_w - self.DISPLAY_W))
        self.offset_float.y += (
                self.player.y - self.offset_float.y +
                self.CONST.y)
        self.offset.y = max(0, min(int(self.offset_float.y),
                                   self.total_h - self.DISPLAY_H))

        current_camera_offset.x, current_camera_offset.y = \
            self.offset.x, self.offset.y


def screen_score(score):
    font = pygame.font.Font('18965.ttf', 40)
    text = font.render("Score: " + str(score), True, (230, 230, 230))
    screen.blit(text, (10, 10))


def health_bar(player):
    fill = (player.health / health_player) * bar_length
    outline_rect = pygame.Rect(20, 50, bar_length, bar_height)
    fill_rect = pygame.Rect(20, 50, fill, bar_height)
    pygame.draw.rect(screen, (255, 51, 51), fill_rect)
    pygame.draw.rect(screen, (255, 255, 255), outline_rect, 2)


def load_level(level_structure):
    with open(level_structure) as f:
        level = f.readlines()
        level = [list(lst.strip()) for lst in level]
    return level


def start_menu():
    menu_bg = pygame.image.load('menu.png')
    show = True
    cont_bt = Button()
    level_bt = Button()
    exit_bt = Button()
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            screen.blit(menu_bg, (0, 0))
            exit_bt.update(860, 640, 'Exit', event, exit_menu)
            if cont_bt.update(860, 440, 'Continue', event, start_game):
                return True
            if level_bt.update(860, 540, 'Levels', event, level_menu):
                return True
            pygame.display.update()
            pygame.display.flip()


def end_menu(score):
    menu_bg = pygame.image.load('menu.png')
    show = True
    exit_to_menu = Button()
    continue_bt = Button()
    next_bt = Button()
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            screen.blit(menu_bg, (0, 0))
            screen.blit(menu_bg, (0, 0))
            font = pygame.font.Font('18965.ttf', 100)
            text = font.render("Score: " + str(score), True, (230, 230, 230))
            screen.blit(text, (700, 300))
            if continue_bt.update(820, 600, 'Restart', event, back_bt):
                show = False
            if exit_to_menu.update(520, 600, 'Menu', event, start_menu):
                show = False
            if next_bt.update(1120, 600, 'Next', event, next_level):
                show = False
            pygame.display.update()
            pygame.display.flip()


def level_menu():
    menu_bg = pygame.image.load('menu.png')
    show_level = True
    start = Button()
    right = Button()
    levels = Button()
    left = Button()
    back = Button()
    start_l = False
    with open('levels\\what_level.txt', 'r') as f:
        level_num = int(f.read())
    count = 0
    while show_level:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            screen.blit(menu_bg, (0, 0))
            if count + 1 < len(all_levels) and count < level_num - 1:
                count += left.update(1200, 540, '>', event, level_add, 80)
            if count - 1 >= 0:
                count -= right.update(660, 540, '<', event, level_add, 80)
            levels.update(740, 540, all_levels[count], event, None, 80)
            if start.update(710, 400, 'Start level', event, start_level, 80,
                            count):
                show_level = False
                start_l = True
            if back.update(800, 680, 'Back', event, back_bt, 80):
                show_level = False
                pygame.display.flip()
            pygame.display.update()
    return start_l


def death_menu(score):
    show_death = True
    menu_bg = pygame.image.load('menu.png')
    exit_to_menu = Button()
    continue_bt = Button()
    while show_death:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            screen.blit(menu_bg, (0, 0))
            font = pygame.font.Font('18965.ttf', 100)
            text = font.render("Score: " + str(score), True, (230, 230, 230))
            screen.blit(text, (700, 300))
            if continue_bt.update(1120, 600, 'Restart', event, back_bt):
                show_death = False
            if exit_to_menu.update(620, 600, 'Menu', event, start_menu):
                show_death = False
            pygame.display.update()
            pygame.display.flip()


class Button:
    def update(self, x, y, text_f, event, action=None, font_size=60,
               extra=None):
        mouse = pygame.mouse.get_pos()
        font = pygame.font.Font('18965.ttf', font_size)
        text = font.render(text_f, True, (230, 230, 230))
        width = font.size(text_f)[0]
        height = font.size(text_f)[1]
        screen.blit(text, (x, y))
        if x < mouse[0] < x + width and y < mouse[1] \
                < y + height:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if action is not None:
                    if text_f == 'Start level':
                        return action(extra)
                    else:
                        return action()
        return 0


def next_level():
    with open('levels\\now.txt', 'r') as f:
        level_num = int(f.read())
    with open('levels\\now.txt', 'w') as f:
        f.write(str(level_num + 1))
    return True


def back_bt():
    return True


def level_add():
    return 1


def start_level(count):
    with open('levels\\now.txt', 'w') as f:
        f.write(str(count + 1))
    return True


def start_game():
    with open('levels\\what_level.txt', 'r') as f:
        level_num = f.read()
    with open('levels\\now.txt', 'w') as f:
        f.write(level_num)
    return True


def exit_menu():
    quit()


if __name__ == '__main__':
    main()
