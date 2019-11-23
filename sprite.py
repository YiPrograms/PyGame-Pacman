import pygame

from pac import Pac, Ghost
from pullet import Pullet

from env import *


class GameSprites():
    def __init__(self, mp):
        self.mp = mp
        self.pac_group = pygame.sprite.RenderUpdates()
        self.ghost_group = pygame.sprite.RenderUpdates()
        self.pullet_group = pygame.sprite.RenderUpdates()

    def new_pac(self, pos):
        self.pac_group.add(Pac(self.mp, pos))

    def new_ghost(self, pos, color):
        self.ghost_group.add(Ghost(self.mp, pos, self.pac_group, color))

    def draw_all(self, screen, dirty):
        def background(surf, rect):
            surf.fill(BG_COLOR, rect)

        self.pac_group.clear(screen, background)
        self.ghost_group.clear(screen, background)
        dirty.extend(self.pac_group.draw(screen))
        for pullet in pygame.sprite.groupcollide(self.pullet_group, self.ghost_group, False, False).keys():
            pullet.draw(screen)
        dirty.extend(self.ghost_group.draw(screen))

        pygame.display.update(dirty)

    def update_all(self):
        self.pac_group.update()
        self.ghost_group.update()
        self.pullet_group.update()

    def change_pac_dir(self, d):
        if self.pac_group:
            self.get_pac().change_dir(d)

    def get_pac(self):
        return self.pac_group.sprites()[0]

    def pac_touch_ghost(self):
        if self.pac_group:
            return pygame.sprite.spritecollide(self.get_pac(), self.ghost_group, False)
        return []

    def eat_pullet(self):
        if self.pac_group:
            return pygame.sprite.spritecollide(self.get_pac(), self.pullet_group, True)
        return []

    def init_pullets(self, screen, road):
        for pos in road:
            self.pullet_group.add(Pullet(pos))

        for pullet in self.pullet_group.sprites():
            pullet.draw(screen)
