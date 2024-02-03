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
            path = tile_images_paths[tile_type]
            if isinstance(path, tuple):
                path = random.choice(path)

            self.image = load_image(path, color_key=-1 if tile_type == 'wall' else None)
            self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))

        self.rect = self.image.get_rect().move(TILE_SIZE * x, TILE_SIZE * y)

        self.mask = pygame.mask.from_surface(self.image)


