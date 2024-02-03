import datetime
from functions import *
from tile import Tile
from tank import Player, Enemy
from mixer import *


def genarate_level(level, all_sprites, tile_sprites, obstacle_sprites, tank_sprites, player_sprite, enemy_sprites,
                   bullet_sprites, explosion_sprite):
    player, enemies = None, 0
    for y in range(len(level)):
        for x in range(len(level[y])):
            Tile(x, y, 'empty', all_sprites, tile_sprites, obstacle_sprites)
            if level[y][x] == '#':
                Tile(x, y, 'wall', all_sprites, tile_sprites, obstacle_sprites)
            elif level[y][x] == '@':
                player = Player(x, y, all_sprites, tank_sprites, obstacle_sprites, bullet_sprites, player_sprite,
                                explosion_sprite)
            elif level[y][x] == '$':
                Enemy(x, y, 'blue', all_sprites, tank_sprites, obstacle_sprites, bullet_sprites, player_sprite,
                      enemy_sprites, explosion_sprite)
                enemies += 1

    return player, enemies


class Level:
    def __init__(self, level):
        # set_misic(r'../data/sounds/music/battle_theme.mp3')
        set_volume(0.1)

        with open(fr'../data/levels/{level}', 'r') as lvl:
            self.level_map = lvl.readlines()
        self.level = level
        self.generate_sprites()

        self.background = load_image(game_background)

        self.battlefield = pygame.Surface((800, 800))
        self.info_screen = pygame.Surface((400, 800))
        self.player, self.enemies = genarate_level(self.level_map, self.all_sprites, self.tile_sprites,
                                                   self.obstacle_sprites, self.tank_sprites, self.player_sprite,
                                                   self.enemy_sprites, self.bullet_sprites, self.explosion_sprites)
        self.init_info_screen()

        self.start_time = datetime.now()
        self.info_data = [None, None, None, None]

        self.game_ended_ticks = 0
        self.wait_ticks = FPS * 2
        self.delta_time = datetime.now() - self.start_time

    def generate_sprites(self):
        self.all_sprites = pygame.sprite.Group()
        self.tile_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.tank_sprites = pygame.sprite.Group()
        self.player_sprite = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.explosion_sprites = pygame.sprite.Group()

    def init_info_screen(self):
        self.info_screen.fill('black')
        pygame.draw.line(self.info_screen, 'gray', (0, 0), (0, 800), 2)
        self.info_screen.blit(pygame.transform.scale(self.player.image, (200, 200)), (100, 10))
        pygame.draw.line(self.info_screen, 'gray', (0, 220), (400, 220), 1)

        info_text = ["Время:", "Противников уничтожено:", "Противников осталось:", f"Уровень:"]

        write_text(self.info_screen, 15, 230, ['Цель: уничтожить всех противников'], 30, 30, 'red')
        write_text(self.info_screen, 15, 300, info_text, 50, 30, 'white')

    def run(self, screen, clock):
        self.battlefield.fill('black')
        self.info_screen.fill('black', (290, 290, 400, 600))
        self.info_screen.fill('black', (14, 499, 400, 700))

        self.player.update(pygame.key.get_pressed())
        self.enemy_sprites.update()
        self.bullet_sprites.update()
        self.explosion_sprites.update()

        self.tile_sprites.draw(self.battlefield)
        self.bullet_sprites.draw(self.battlefield)
        self.tank_sprites.draw(self.battlefield)
        self.explosion_sprites.draw(self.battlefield)

        screen.blit(self.battlefield, (0, 0))

        time_now = datetime.now()

        self.info_data[0] = f'{self.delta_time.seconds}.{str(self.delta_time.microseconds)[:2]}'
        self.info_data[1] = str(self.player.enemies_destroyed)
        self.info_data[2] = str(len(self.enemy_sprites))
        self.info_data[3] = str(self.level)

        write_text(self.info_screen, 290, 300, self.info_data, 50, 30, 'white')
        write_text(self.info_screen, 15, 500, ['Снаряд готов' if self.player.reloaded else 'Перезарядка'], 50, 30,
                   'white' if self.player.reloaded else 'red')

        screen.blit(self.info_screen, (800, 0))

        pygame.display.flip()
        clock.tick(FPS)

        if self.player.game_over or not len(self.enemy_sprites):
            self.game_ended_ticks += 1
        else:
            self.delta_time = time_now - self.start_time

        if self.game_ended_ticks == self.wait_ticks:
            return ('loose', self.info_data) if self.player.game_over else ('win', self.info_data)
        return ' '