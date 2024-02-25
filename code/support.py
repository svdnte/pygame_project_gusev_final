import io

import pygame
import os
import sys
import random
from datetime import datetime
import sqlite3
from time import sleep

version = 0.2

SCALE = 1

FPS = 60
SIZE = WIDTH, HEIGHT = 1200 * SCALE, 800 * SCALE
WIDTH2, HEIGHT2 = 800 * SCALE, 800 * SCALE


intro_text = [
    "ТРЕНИРОВКА",
    "КАМПАНИЯ"
    # "СОЗДАТЬ УРОВЕНЬ",
    # "НАСТРОЙКИ",
    # "ПОМОЩЬ"
]


tile_images_paths = {
    'wall': (
        r'../data/images/object_images/metal_box/metal_box.png',
        r'../data/images/object_images/metal_box/metal_box1.png',
    ),
    'sand': (
        r'../data/images/object_images/sand/sand1.png',
        r'../data/images/object_images/sand/sand2.png',
        r'../data/images/object_images/sand/sand3.png'
    )
}

game_background = r'../data/images/game_background.png'
bullet_image = r'../data/images/bullet.png'
explosion_image = r'../data/images/explosion.png'


TILE_SIZE = int(50 * SCALE)
VELOCITY = TILE_SIZE / FPS * SCALE


directions = ['N', 'S', 'W', 'E']


def get_data():
    try:
        with open(r'../data/data.txt', 'w', encoding='utf8') as file:
            data = file.readlines()
            for line in data:
                exec(line)
    except io.UnsupportedOperation:
        print('Не удалось открыть текстовый файл с данными, возможно, он пуст')


get_data()
