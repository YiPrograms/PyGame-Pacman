

FPS = 60

MAP_WIDTH = 19
MAP_HEIGHT = 21
BLOCK_SIZE = 45

BG_COLOR = (0, 0, 0)

ASSETS_DIR = "./assets"

DIR = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]
REV_DIR = [0, 2, 1, 4, 3]


import pygame
from os import path
BLANK_IMAGE = pygame.Surface((BLOCK_SIZE-8, BLOCK_SIZE-8))

PAC_IMAGE = pygame.transform.scale(pygame.image.load(path.join(ASSETS_DIR, "pac.png")),
                                  (BLOCK_SIZE-8, BLOCK_SIZE-8))
        
GHOST_RED = pygame.transform.scale(pygame.image.load(path.join(ASSETS_DIR, "ghost-red.png")),
                                  (BLOCK_SIZE-8, BLOCK_SIZE-8))

GHOST_GREEN = pygame.transform.scale(pygame.image.load(path.join(ASSETS_DIR, "ghost-green.png")),
                                  (BLOCK_SIZE-8, BLOCK_SIZE-8))

GHOST_YELLOW = pygame.transform.scale(pygame.image.load(path.join(ASSETS_DIR, "ghost-yellow.png")),
                                  (BLOCK_SIZE-8, BLOCK_SIZE-8))

GHOST_TUX = pygame.transform.scale(pygame.image.load(path.join(ASSETS_DIR, "ghost-tux.png")),
                                  (BLOCK_SIZE-8, BLOCK_SIZE-8))

GHOST_IMAGES = [GHOST_RED, GHOST_GREEN, GHOST_YELLOW, GHOST_TUX]

GHOST_AFRAID = pygame.transform.scale(pygame.image.load(path.join(ASSETS_DIR, "ghost-afraid.png")),
                                  (BLOCK_SIZE-8, BLOCK_SIZE-8))

GHOST_EYES = pygame.transform.scale(pygame.image.load(path.join(ASSETS_DIR, "ghost-eyes.png")),
                                  (BLOCK_SIZE-8, BLOCK_SIZE-8))
