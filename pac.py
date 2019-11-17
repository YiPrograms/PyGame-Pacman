from os import path

import pygame
from env import *


class Pac(pygame.sprite.Sprite):
    def __init__(self, texture):
        super().__init__(self)
        self.pos = {
            'x': 0,
            'y': 0
        }
        self.speed = 1
        self.target = (0, 0)
        self.texture = pygame.image.load(path.join(ASSETS_DIR, texture))

    def move(self):
        pass

    def set_target(self, row, column):
        self.target = (row, column)

    def _search(self):
        pass

    def on_destroy(self):
        pass

    def destroy(self):
        self.on_destroy()
        self.kill()
