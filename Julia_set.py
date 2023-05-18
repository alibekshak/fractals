import pygame
import os

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# sets the position of the pygame window
x = 20
y = 40
os.environ["SDL_VIDEo_WINDOW_POS"] = "%d, %d" % (x,y)

pygame.init()

W = 1200
H = 600

sc = pygame.display.set_mode((W, H))
pygame.display.set_caption("Julia set")
sc.fill(WHITE)

FPS = 30
clock = pygame.time.Clock()


c = complex(-0.2, 0.75) # размер области рисования
P = 200  # области рисования (пиксели)
scale = P / 2 # маштабный коэффициент 
n_iter = 100

for y in range(-P, P):
    for x in range(-P, P):
        a = x/ scale
        b = y / scale
        z = complex(a, b)
        for n in range(n_iter):
            z = z ** 2 + c
            if abs(z) > 2:
                break
        else:
            pygame.draw.circle(sc, BLACK, (x + P, y + P), 1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    pygame.display.flip()
    clock.tick(FPS)