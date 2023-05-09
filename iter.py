import pygame
import numpy as np
import os

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Для появления окна
x = 20
y = 40
os.environ["SDL_VIDEO_POS"] = "%d, %d" % (x, y)

pygame.init()

W = 1200
H = 600

sc = pygame.display.set_mode((W, H)) #размер экрана
pygame.display.set_caption("Итеративная функция")
sc.fill(WHITE)

surf_e = pygame.Surface((200, 200))


FPS = 30
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    pygame.display.update()
    clock.tick(FPS)