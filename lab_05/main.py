import pygame as pg
import random
import time
import math
from math import sin, cos


def rotate(x1, y1, x2, y2, degrees):
    x_new = cos(degrees) * (x1 - x2) - sin(degrees) * (y1 - y2) + x2
    y_new = sin(degrees) * (x1 - x2) + cos(degrees) * (y1 - y2) + y2

    return x_new, y_new


class MatrixFigures:
    def __init__(self, app):
        self.app = app
        self.figure_size = 40
        self.screen = app.screen

        self.columns = app.width // self.figure_size
        self.drops = [1 for i in range(0, self.columns)]

    def draw(self):
        deg = math.pi / 6

        for i in range(0, len(self.drops) - 1):
            pos = i * self.figure_size + self.figure_size // 2, \
                  (self.drops[i] - 1) * self.figure_size
            alpha = random.randint(0, 10)
            x_new_1, y_new_1 = rotate(pos[0] - self.figure_size // 3, pos[1] - self.figure_size // 5,
                                      pos[0], pos[1], alpha * deg)
            x_new_2, y_new_2 = rotate(pos[0], pos[1] - self.figure_size // 3,
                                      pos[0], pos[1], alpha * deg)
            x_new_3, y_new_3 = rotate(pos[0] + self.figure_size // 3, pos[1] - self.figure_size // 5,
                                      pos[0], pos[1], alpha * deg)
            x_new_4, y_new_4 = rotate(pos[0] + self.figure_size // 3, pos[1] + self.figure_size // 5,
                                      pos[0], pos[1], alpha * deg)
            x_new_5, y_new_5 = rotate(pos[0], pos[1] + self.figure_size // 3,
                                      pos[0], pos[1], alpha * deg)
            x_new_6, y_new_6 = rotate(pos[0] - self.figure_size // 3, pos[1] + self.figure_size // 5,
                                      pos[0], pos[1], alpha * deg)

            if alpha % 2:
                pg.draw.polygon(self.app.surface, (0, random.randint(0, 255), 0), [[x_new_1, y_new_1],
                                                                                   [x_new_2, y_new_2],
                                                                                   [x_new_3, y_new_3],
                                                                                   [x_new_4, y_new_4],
                                                                                   [x_new_5, y_new_5],
                                                                                   [x_new_6, y_new_6]], 3)
            elif alpha > 7:
                pg.draw.circle(self.app.surface, (0, random.randint(0, 255), 0), (pos[0],
                                                                                  pos[1]), self.figure_size // 3, 3)
            else:
                pg.draw.lines(self.app.surface, (0, random.randint(0, 255), 0), True, [[x_new_6, y_new_6],
                                                                                       [x_new_4, y_new_4],
                                                                                       [x_new_2, y_new_2]], 3)

            if self.drops[i] * self.figure_size > app.height and random.uniform(0, 1) > 0.975:
                self.drops[i] = 0
            self.drops[i] += 1

    def run(self):
        self.draw()


class MatrixApp:
    def __init__(self):
        self.res = self.width, self.height = 1920, 1080
        pg.init()
        self.screen = pg.display.set_mode(self.res)
        self.surface = pg.Surface(self.res, pg.SRCALPHA)
        self.clock = pg.time.Clock()
        pg.display.set_mode((0, 0), pg.FULLSCREEN)
        self.matrix_figures = MatrixFigures(self)
        self.bg = Background('matrix_bg.jpg', (0, 0))

    def draw(self):
        self.surface.fill((0, 0, 0, 15))
        self.matrix_figures.run()
        self.screen.blit(self.surface, (0, 0))

    def run(self):
        self.screen.blit(self.bg.image, self.bg.rect)
        while True:
            time.sleep(0.04)
            self.draw()
            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            pg.display.flip()
            self.clock.tick(60)


class Background(pg.sprite.Sprite):
    def __init__(self, image_file, location):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(image_file).convert()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


if __name__ == '__main__':
    app = MatrixApp()
    app.run()
