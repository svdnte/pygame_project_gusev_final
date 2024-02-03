import pygame.mixer

from functions import *
from support import *
from bullet import Bullet
from explosion import Explosion


class Tank(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image(fr'../data/images/vehicle_images/green_tank.png', color_key=-1),
                                   (TILE_SIZE * 0.8, TILE_SIZE * 0.8))

    def __init__(self, x, y, all_sprites, tank_sprites, obstacle_sprites, bullet_sprites, player_sprite,
                 explosion_sprites):
        super().__init__(all_sprites, tank_sprites)

        self.mask = pygame.mask.from_surface(self.image)

        self.reloaded = False

        self.V = TILE_SIZE / 50
        self.direction = 'N'

        self.shot_time = -2000
        self.reloading_time = 2000

        self.original_image = self.image

        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x * TILE_SIZE, y * TILE_SIZE)

        self.obstacle_sprites = obstacle_sprites
        self.tank_sprites = tank_sprites
        self.bullet_sprites = bullet_sprites
        self.all_sprites = all_sprites
        self.player_sprite = player_sprite
        self.explosion_sprites = explosion_sprites

        # self.shoot_sound = pygame.mixer.Sound(r'../data/sounds/effects/shoot.wav')
        self.shoot_sound = pygame.mixer.Sound(r'C:\Users\gunna\PycharmProjects\pygame_project_gusev_final\data\sounds\effects\jg-032316-sfx-8-bit-punch.mp3')
        self.explosion_sound = pygame.mixer.Sound(r"C:\Users\gunna\Downloads\jg-032316-sfx-8-bit-hit-6.mp3")
        self.explosion_sound.set_volume(0.34)

    def update(self, key_list):
        self.check_reload()

        # Меняем направление движения
        if key_list[pygame.K_w] or key_list[pygame.K_UP]:
            self.rect.y -= self.V
            self.direction = 'N'
            self.direction_changed()
            if self.rect.y < 0:
                self.rect.y += self.V * 2

        if key_list[pygame.K_s] or key_list[pygame.K_DOWN]:
            self.rect.y += self.V
            self.direction = 'S'
            self.direction_changed()
            if self.rect.y + self.rect.h > 800:
                self.rect.y -= self.V * 2

        if key_list[pygame.K_a] or key_list[pygame.K_LEFT]:
            self.rect.x -= self.V
            self.direction = 'W'
            self.direction_changed()
            if self.rect.x < 0:
                self.rect.x += self.V * 2

        if key_list[pygame.K_d] or key_list[pygame.K_RIGHT]:
            self.rect.x += self.V
            self.direction = 'E'
            self.direction_changed()
            if self.rect.x + self.rect.w > 800:
                self.rect.x -= self.V * 2

        # Создаем пулю
        if key_list[pygame.K_SPACE]:
            self.shoot()

        self.ejection()

    def shoot(self):
        if self.reloaded:
            Bullet(self, self.direction, self.rect.x, self.rect.y, self.all_sprites, self.bullet_sprites,
                   self.obstacle_sprites, self.tank_sprites, self.player_sprite)
            self.shoot_sound.play()
            self.shot_time = pygame.time.get_ticks()
            self.reloaded = False

    def check_reload(self):
        if pygame.time.get_ticks() - self.shot_time >= self.reloading_time:
            self.reloaded = True

    def ejection(self):
        coll = self.check_collide()
        if coll:
            direction = self.check_collide_direction(coll)
            while direction:
                conv = self.convert(direction)
                move = -conv[0], -conv[1]
                self.make_move(*move)

                direction = self.check_collide_direction(coll)
            return True
        return False

    def direction_changed(self):
        if self.direction == 'N':
            self.image = self.original_image
        elif self.direction == 'E':
            self.image = pygame.transform.rotate(self.original_image, 270)
        elif self.direction == 'S':
            self.image = pygame.transform.rotate(self.original_image, 180)
        else:
            self.image = pygame.transform.rotate(self.original_image, 90)
        self.mask = pygame.mask.from_surface(self.image)

    def check_collide(self):
        for sprite in self.obstacle_sprites:
            if pygame.sprite.collide_mask(self, sprite):
                return sprite
        for sprite in self.tank_sprites:
            if pygame.sprite.collide_mask(self, sprite):
                if sprite != self:
                    return sprite
        return None

    def destroy(self):
        Explosion(self.rect.x, self.rect.y, self.all_sprites, self.explosion_sprites)
        self.explosion_sound.play()
        self.kill()

    def convert(self, direction):
        if direction == 'N':
            return 0, -1
        elif direction == 'S':
            return 0, 1
        elif direction == 'W':
            return -1, 0
        elif direction == 'E':
            return 1, 0

    def check_collide_direction(self, obj):
        r = obj.rect
        s = self.rect
        if r.collidepoint(s.x, s.y + TILE_SIZE / 8) or r.collidepoint(s.x, s.y + s.h - TILE_SIZE / 8):
            return 'W'
        if r.collidepoint(s.x + s.w, s.y + TILE_SIZE / 8) or r.collidepoint(s.x + s.w, s.y + s.h - TILE_SIZE / 8):
            return 'E'
        if r.collidepoint(s.x + 2, s.y) or r.collidepoint(s.x + s.w - 2, s.y):
            return 'N'
        if r.collidepoint(s.x + 2, s.y + s.h) or r.collidepoint(s.x + s.w - 2, s.y + s.h):
            return 'S'

    def make_move(self, x, y):
        self.rect = self.rect.move(self.V * x, self.V * y)

    def get_image(self):
        return self.image


class Player(Tank):
    def __init__(self, x, y, all_sprites, tank_sprites, obstacle_sprites, bullet_sprites, player_sprite,
                 explosion_sprite):
        super().__init__(x, y, all_sprites, tank_sprites, obstacle_sprites, bullet_sprites, player_sprite,
                         explosion_sprite)
        self.add(player_sprite)
        self.game_over = False
        self.enemies_destroyed = 0

        self.shoot_sound.set_volume(0.5)

    def bullet_hit(self, obj):
        self.enemies_destroyed += 1

    def destroy(self):
        Explosion(self.rect.x, self.rect.y, self.all_sprites, self.explosion_sprites)
        self.explosion_sound.play()
        self.game_over = True
        self.kill()


class Enemy(Tank):
    def __init__(self, x, y, color, all_sprites, tank_sprites, obstacle_sprites, bullet_sprites, player_sprite,
                 enemy_sprites, explosion_sprite):
        super().__init__(x, y, all_sprites, tank_sprites, obstacle_sprites, bullet_sprites, player_sprite,
                         explosion_sprite)
        self.add(enemy_sprites)

        self.obstacle_sprites = obstacle_sprites
        self.player_sprite = player_sprite

        self.original_image = \
            pygame.transform.scale(load_image(fr'../data/images/vehicle_images/{color}_tank.png', color_key=-1),
                                   (TILE_SIZE * 0.8, TILE_SIZE * 0.8))
        self.image = self.original_image

        self.direction = random.choice(directions)
        self.direction_changed()

        self.shoot_sound.set_volume(0.3)

    def update(self):
        self.check_reload()

        self.move(*self.convert(self.direction))
        if self.find_target():
            self.shoot()

    def move(self, x, y):
        self.rect = self.rect.move(self.V * x, self.V * y)

        ej = self.ejection()
        if ej:
            self.change_direction()

        if not 0 < self.rect.x < 800 - self.rect.w or not 0 < self.rect.y < 800 - self.rect.h:
            move = self.convert(self.direction)
            self.make_move(-move[0] * self.V, -move[1] * self.V)
            self.change_direction()

    def change_direction(self):
        d = directions[::]
        d.remove(self.direction)
        self.direction = random.choice(d)
        self.direction_changed()

    def find_target(self):
        if self.direction == 'N':
            start = self.rect.y
            finish = 0
            step = int(-TILE_SIZE * 0.8 + 2)
        elif self.direction == 'S':
            start = self.rect.y + self.rect.h
            finish = 800
            step = int(TILE_SIZE * 0.8 - 2)
        elif self.direction == 'W':
            start = self.rect.x
            finish = 0
            step = int(-TILE_SIZE * 0.8 + 2)
        else:
            start = self.rect.x + self.rect.w
            finish = 800
            step = int(TILE_SIZE * 0.8 + 2)

        if self.direction in ('N', 'S'):
            for i in range(start, finish, step):
                for obst_sprite in self.obstacle_sprites:
                    if obst_sprite.rect.collidepoint(self.rect.x + self.rect.h // 2, i):
                        break
                for player in self.player_sprite:
                    if player.rect.collidepoint(self.rect.x + self.rect.h // 2, i):
                        self.shoot()

        else:
            for i in range(start, finish, step):
                for obst_sprite in self.obstacle_sprites:
                    if obst_sprite.rect.collidepoint(i, self.rect.y + self.rect.h // 2):
                        break
                for player in self.player_sprite:
                    if player.rect.collidepoint(i, self.rect.y + self.rect.h // 2):
                        self.shoot()

    def bullet_hit(self, obj):
        pass
