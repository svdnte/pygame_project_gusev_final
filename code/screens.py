import pygame

from support import *

pygame.mixer.pre_init(channels=5)
pygame.init()
pygame.display.set_caption('Game')
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

from functions import *
from tile import Tile
from level import *
from mixer import *


def start_screen():
    background = pygame.transform.scale(pygame.image.load(r'../data/images/background.png'), (WIDTH, HEIGHT))
    screen.blit(background, (0, 0))

    intro_text_cords = {}

    text_cord = 50 * SCALE
    for line in intro_text:
        font = pygame.font.Font(None, 50)
        st_rendered = font.render(line, 1, pygame.Color('black'))

        st_rect = st_rendered.get_rect()
        st_rect.x = 20 * SCALE
        st_rect.top = text_cord
        text_cord += st_rect.height + 20

        screen.blit(st_rendered, st_rect)

        intro_text_cords[line] = st_rect

    font = pygame.font.Font(None,int(65 * SCALE))
    st_rendered = font.render('НАЗВАНИЕ ИГРЫ', 1, pygame.Color('black'))
    st_rect = st_rendered.get_rect()
    st_rect.x = 600 * SCALE
    st_rect.y = 80 * SCALE

    screen.blit(st_rendered, st_rect)

    pygame.display.flip()

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                for name, cords in intro_text_cords.items():
                    if cords.collidepoint(ev.pos):
                        if name == 'ТРЕНИРОВКА':
                            level_select_screen()
                            return
                        elif name == 'КАМПАНИЯ':
                            start_campaign()
                        elif name == 'СОЗДАТЬ УРОВЕНЬ':
                            # create_level()
                            return
                        elif name == 'НАСТРОЙКИ':
                            open_settings()
                            return
                        elif name == 'ПОМОЩЬ':
                            open_help_window()
                            return
        clock.tick(FPS)


def open_settings():
    # сделать регулировку звука общую, музыки, эффектов и тд.
    # возможно сделать несколько разделов настроек, например: графика, общие, звук
    print(1)


def open_help_window():
    # помощь в управлении, справка по игре
    print(2)


def start_campaign():
    def begin_level(level):
        screen.fill('black')
        write_text(screen, 0, 400 * SCALE, [level], 0, 50, 'white', x_centered=True)

        pygame.display.flip()
        sleep(2)

    levels = os.listdir(r'../data/levels/')
    for level in levels:
        begin_level(level)
        game(level, mode='campaign')

    begin_level('123')


def level_select_screen():
    screen.fill('black')
    offset = 0

    write_text(screen, 0, 20 * SCALE, ['ВЫБЕРИТЕ УРОВЕНЬ'], 10 * SCALE, 50 * SCALE, 'white', x_centered=True)
    exit_btn_cords = write_text(screen, 100 * SCALE, HEIGHT2 - 50 * SCALE, ['Выйти в меню'], 1 * SCALE, 50 * SCALE, 'white')
    left_btn = write_text(screen, 35 * SCALE, 350 * SCALE, ['<'], 1 * SCALE, 70 * SCALE, 'white')
    right_btn = write_text(screen, WIDTH - 70 * SCALE, 350 * SCALE, ['>'], 1 * SCALE, 70 * SCALE, 'white')

    font = pygame.font.Font(None, 50)

    levels = os.listdir(r'../data/levels/')
    level_list = {}

    def show_levels(offset=0):
        for i in range(2):
            for j in range(3):
                try:
                    with open(f'../data/levels/{levels[i * 3 + j + offset]}', 'r') as level:
                        st_rendered = font.render(levels[i * 3 + j + offset][:-4], 1, pygame.Color('white'))
                        st_rect = st_rendered.get_rect()
                        st_rect.x = WIDTH // 4 + WIDTH // 4 * j - st_rect.width // 2
                        st_rect.y = HEIGHT // 3 + HEIGHT // 3 * i - st_rect.height // 2

                        screen.blit(st_rendered, st_rect)

                        level_list[levels[i * 3 + j + offset]] = st_rect

                except IndexError:
                    break

    while True:
        screen.fill('black')

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                for lvl, cords in level_list.items():
                    if cords.collidepoint(ev.pos):
                        game(lvl)
                        return
                if to_rect(exit_btn_cords).collidepoint(ev.pos):
                    start_screen()
                if to_rect(left_btn).collidepoint(ev.pos):
                    level_list = {}

                    offset -= 6
                    if offset < 0:
                        offset = 0
                if to_rect(right_btn).collidepoint(ev.pos):
                    level_list = {}

                    offset += 6

        show_levels(offset)
        write_text(screen, 0, 20, ['ВЫБЕРИТЕ УРОВЕНЬ'], 10, 50 * SCALE, 'white', x_centered=True)
        exit_btn_cords = write_text(screen, 100, HEIGHT2 - 50 * SCALE, ['Выйти в меню'], 1, 50 * SCALE, 'white')
        left_btn = write_text(screen, 35, 350, ['<'], 1, 70 * SCALE, 'white')
        right_btn = write_text(screen, WIDTH - 70, 350, ['>'], 1, 70 * SCALE, 'white')

        pygame.display.flip()
        clock.tick(FPS)


# def create_level():
#     screen.fill('black')
#
#     write_text(screen, 0, 20, ['СОЗДАТЬ УРОВЕНЬ'], 10, 50, 'white', x_centered=True)
#
#     # сделать поле клеточное как в первых пайгейм уроках, на него ставятся препятствия, игрок, противники.
#
#     while True:
#         for ev in pygame.event.get():
#             if ev.type == pygame.QUIT:
#                 terminate()
#
#         pygame.display.flip()
#         clock.tick(FPS)


def end_game(result, level, mode='training'):
    con = sqlite3.connect(r'../data/database/db.db')
    cur = con.cursor()

    print(result)

    # добвить подсчет очков, вохможность ставить рекорд, запись данных, история матчей
    screen.fill('black')
    write_text(screen, 0, 100 * SCALE, ['Победа!' if result[0] == 'win' else 'Поражение'], 1, 60 * SCALE, 'blue' if result[0] == 'win'
                                                                                            else 'red', x_centered=True)
    write_text(screen, 0, 160 * SCALE, [f'Уровень: {result[1][3]}'], 1, 50 * SCALE, 'white', x_centered=True)
    write_text(screen, 0, 220 * SCALE, [f'Противников уничтожено: {result[1][1]}'], 1, 50 * SCALE, 'white', x_centered=True)
    write_text(screen, 0, 280 * SCALE, [f'Время: {result[1][0]} секунд'], 1, 50 * SCALE, 'white', x_centered=True)

    games = cur.execute(f"""SELECT * FROM battles WHERE level = '{level}' and result = 'win'""").fetchall()

    if result[0] == 'win':
        if games:
            best_time = sorted(games, key=lambda x: x[3])[0][3]
            print(best_time)

            if float(result[1][0]) < best_time:
                write_text(screen, 0, 340 * SCALE, [f'Новый рекорд!'], 1, 50 * SCALE, 'white', x_centered=True)
            else:
                write_text(screen, 0, 340 * SCALE, [f'Рекордное время: {best_time} секунд'], 1, 50, 'white', x_centered=True)
        else:
            write_text(screen, 0, 340 * SCALE, [f'Новый рекорд!'], 1, 50 * SCALE, 'white', x_centered=True)

    else:
        if games:
            best_time = sorted(games, key=lambda x: x[3])[0][3]
            write_text(screen, 0, 340 * SCALE, [f'Рекордное время: {best_time} секунд'], 1, 50 * SCALE, 'white', x_centered=True)

    con.execute(f"""INSERT into battles (result, killed, time, level) values ('{result[0]}', {result[1][1]}, 
{result[1][0]}, '{result[1][3]}')""")
    con.commit()

    if mode == 'training' or result[0] == 'loose':
        exit_btn_cords = write_text(screen, 100 * SCALE, 650 * SCALE, ['Выйти в меню'], 1, 50 * SCALE, 'white')
        print(1)

        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    terminate()
                if ev.type == pygame.MOUSEBUTTONDOWN and to_rect(exit_btn_cords).collidepoint(ev.pos):
                    start_screen()
                    return
            pygame.display.flip()
    else:
        pygame.display.flip()
        return


def game(level, mode='training'):
    pygame.mixer.music.stop()

    screen.blit(load_image(game_background), (0, 0))

    level1 = Level(level)

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                level1.clicked(ev.pos)
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_v:
                    level1.set_pause()
                elif ev.key == pygame.K_ESCAPE:
                    level1.exit = True

        move = level1.run(screen, clock)

        if move:

            if move[0] in ('loose', 'win'):
                if mode == 'training':
                    set_misic(r'../data/sounds/music/main_theme.mp3')
                    end_game(move, level)
                else:
                    end_game(move, level, mode='campaign')
                    return
            elif move == 'exit':
                start_screen()


def main():
    # set_misic(r'../data/sounds/music/main_theme.mp3')
    start_screen()
