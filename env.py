

FPS = 60

MAP_WIDTH = 19
MAP_HEIGHT = 21
BLOCK_SIZE = 45

ASSETS_DIR = "./assets"

DIR = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]

import pygame
from os import path
PAC_IMAGE = pygame.transform.scale(pygame.image.load(path.join(ASSETS_DIR, "pac.png")),
                                  (BLOCK_SIZE-8, BLOCK_SIZE-8))
        
RGHOST_IMAGE = pygame.transform.scale(pygame.image.load(path.join(ASSETS_DIR, "ghost-red.png")),
                                  (BLOCK_SIZE-8, BLOCK_SIZE-8))
