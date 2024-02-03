import pygame
import os
import sys
import random
from datetime import datetime
import sqlite3

FPS = 60
SIZE = WIDTH, HEIGHT = 1200, 800
WIDTH2, HEIGHT2 = 800, 800


intro_text = [
    "ИГРАТЬ",
    # "СОЗДАТЬ УРОВЕНЬ",
    # "НАСТРОЙКИ",
    # "ПОМОЩЬ"
]


tile_images_paths = {
    'wall': r'../data/images/object_images/metal_box.png',
    'sand': (
        r'../data/images/object_images/sand/sand1.png',
        r'../data/images/object_images/sand/sand2.png',
        r'../data/images/object_images/sand/sand3.png'
    )
}

game_background = r'../data/images/game_background.png'
bullet_image = r'../data/images/bullet.png'
explosion_image = r'../data/images/explosion.png'


TILE_SIZE = 50


directions = ['N', 'S', 'W', 'E']
