# Информация о программе:
# 
# [ЗАЩИТА ЛАБОРАТОРНОЙ РАБОТЫ]
# 
# Движение вращающегося правильного шестиугольника по параболе
# Реализован в рамках курса по "Программированию на Python".
# 
# Автор: Постнов Степан Андреевич, студент МГТУ им. Н.Э.Баумана


from math import sin, cos
import pygame
from random import randint

width, height = 600, 720
color_background = (randint(0, 255), randint(0, 255), randint(0, 255))
fps = 30

pygame.init()
surf = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()


def generate_coord(x0, y0, wid, hei):
    # print(x0, y0, wid, hei)
    coord_1 = [x0 - wid // 2, y0 - hei // 4]
    coord_2 = [x0, y0 - hei // 2]
    coord_3 = [x0 + wid // 2, y0 - hei // 4]
    coord_4 = [x0 + wid // 2, y0 + hei // 4]
    coord_5 = [x0, y0 + hei // 2]
    coord_6 = [x0 - wid // 2, y0 + hei // 4]
    return [coord_1, coord_2, coord_3, coord_4, coord_5, coord_6, x0, y0]


width_fig = 30
height_fig = 30
speed = 1
x_0 = 0
y_0 = 0
coords_fig = generate_coord(0, width, width_fig, height_fig)
# print(coords_fig)
color_fig = (randint(0, 255), randint(0, 255), randint(0, 255))
angl = 0


def move(x, spd):
    div = 200
    new_x = x + spd
    new_y = new_x ** 2 / div
    return [new_x, new_y]


def rotate(c, cd, angle):
    x = c[0]
    y = c[1]
    x0 = cd[0]
    y0 = cd[1]
    new_x = (x - x0) * cos(angle) - (y - y0) * sin(angle) + x0
    new_y = (x - x0) * sin(angle) + (y - y0) * cos(angle) + y0
    return [new_x, new_y]


while True:
    clock.tick(fps)
    [exit() for i in pygame.event.get() if i.type == pygame.QUIT]

    surf.fill(color_background)

    coords_fig = generate_coord(coords_fig[6], coords_fig[7], width_fig, height_fig)
    coords_fig[0] = rotate(coords_fig[0], [coords_fig[6], coords_fig[7]], angl)
    coords_fig[1] = rotate(coords_fig[1], [coords_fig[6], coords_fig[7]], angl)
    coords_fig[2] = rotate(coords_fig[2], [coords_fig[6], coords_fig[7]], angl)
    coords_fig[3] = rotate(coords_fig[3], [coords_fig[6], coords_fig[7]], angl)
    coords_fig[4] = rotate(coords_fig[4], [coords_fig[6], coords_fig[7]], angl)
    coords_fig[5] = rotate(coords_fig[5], [coords_fig[6], coords_fig[7]], angl)
    angl += 0.1
    coords_fig[6], coords_fig[7] = move(coords_fig[6], speed)

    coords_fig[7] = width - coords_fig[7]

    pygame.draw.polygon(surf, color_fig, coords_fig[:6])

    pygame.display.flip()
