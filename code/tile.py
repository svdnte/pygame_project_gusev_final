import random

import pygame

from support import *
from functions import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_type, all_sprites, tile_sprites, obstacle_sprites):
        super().__init__(all_sprites, tile_sprites)

        if tile_type == 'wall':
            self.add(obstacle_sprites)

        if tile_type == 'empty':
            self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        else:
            self.path = tile_images_paths[tile_type]
            if isinstance(self.path, tuple):
                path = self.path[0]
            else:
                path = self.path

            self.image = load_image(path, color_key=-1 if tile_type == 'wall' else None)
            self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))

        self.rect = self.image.get_rect().move(TILE_SIZE * x, TILE_SIZE * y)

        self.mask = pygame.mask.from_surface(self.image)

        self.hit_counter = 0

    def hit(self):
        self.hit_counter += 1

        if self.hit_counter == 2:
            self.kill()
        else:
            self.image = load_image(self.path[self.hit_counter], color_key=-1)
            self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))




