import pygame

pygame.init()

from env import *


def main():
    screen = pygame.display.set_mode((MAP_WIDTH * MAP_SIZE, MAP_HEIGHT * MAP_SIZE))
    pygame.display.set_caption("Pacman")

    clock = pygame.time.Clock()

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()


if __name__ == "__main__":
    while True:
        running = True
        main()
