import pygame

from env import *

class Pullet(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.x = int(pos[1]*BLOCK_SIZE + BLOCK_SIZE/2)
        self.y = int(pos[0]*BLOCK_SIZE + BLOCK_SIZE/2)
        self.rect = pygame.Rect(pos, (BLOCK_SIZE//4, BLOCK_SIZE//4))
        self.rect.centerx = self.x
        self.rect.centery = self.y

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), BLOCK_SIZE//8)