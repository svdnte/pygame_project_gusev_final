from support import *


def load_image(name, color_key=None):
    fullname = name

    if not os.path.isfile(fullname):
        print(f"Файл {fullname} не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def write_text(screen, x, y, text, step, size, color, x_centered=False):
    font = pygame.font.Font(None, int(size))

    rect_and_line = []

    text_cord_y = y
    for ind, line in enumerate(text):
        st_rendered = font.render(line, 1, color)
        st_rect = st_rendered.get_rect()
        st_rect.y = text_cord_y + step * ind
        if x_centered:
            st_rect.x = screen.get_width() // 2 - st_rect.w // 2
        else:
            st_rect.x = x

        screen.blit(st_rendered, st_rect)

        rect_and_line.append((line, (st_rect.x, st_rect.y, st_rect.w, st_rect.h)))

    return rect_and_line


def to_rect(data):
    return pygame.Rect(data[0][1])