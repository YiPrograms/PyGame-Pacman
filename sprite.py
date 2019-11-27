import pygame

from pac import Pac, Ghost
from pullet import SPullet, PPullet

from env import *


class GameSprites():
    def __init__(self, mp):
        self.mp = mp
        self.pac_group = pygame.sprite.RenderUpdates()
        self.ghost_group = pygame.sprite.RenderUpdates()
        self.pullet_group = pygame.sprite.RenderUpdates()
        self.s_pullet_group = pygame.sprite.RenderUpdates()
        self.p_pullet_group = pygame.sprite.RenderUpdates()
        
        self.splash_group = pygame.sprite.Group()

    def new_pac(self, pos):
        pac = Pac(self.mp, pos)
        self.pac_group.add(pac)
        self.splash_group.add(pac)

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

    def change_pac_dir(self, d):
        if self.pac_group:
            self.get_pac().change_dir(d)

    def get_pac(self):
        return self.pac_group.sprites()[0]
    
    def splash(self):
        for spr in self.splash_group:
            if spr.splash > 0:
                spr.splash -= 1
                if spr.splash & 1:
                    spr.image = BLANK_IMAGE
                else:
                    spr.image = spr.org_img
    
    def set_power(self, power):
        if power:
            for ghost in self.ghost_group:
                if not ghost.going_home:
                    ghost.afraid = True
                    ghost.image = GHOST_AFRAID
                    ghost.set_speed(2)
        else:
            for ghost in self.ghost_group:
                if ghost.afraid:
                    ghost.afraid = False
                    ghost.image = GHOST_IMAGES[ghost.color]
                    self.splash_group.remove(ghost)
                    ghost.set_speed(3)
                
    def power_almost_over(self):
        for ghost in self.ghost_group:
            if ghost.afraid:
                self.splash_group.add(ghost)
                ghost.splash = 16

    def pac_touch_ghost(self):
        if self.pac_group:
            return pygame.sprite.spritecollide(self.get_pac(), self.ghost_group, False)
        return []

    def eat_small_pullet(self):
        if self.pac_group:
            return pygame.sprite.spritecollide(self.get_pac(), self.s_pullet_group, True)
        return []
    
    def eat_power_pullet(self):
        if self.pac_group:
            return pygame.sprite.spritecollide(self.get_pac(), self.p_pullet_group, True)
        return []
    
    def eat_ghost(self, ghost):
        if ghost in self.splash_group.sprites():
            self.splash_group.remove(ghost)
        ghost.go_home()

    def init_pullets(self, screen, small_pul, power_pul):
        for pos in small_pul:
            new_pul = SPullet(pos)
            self.pullet_group.add(new_pul)
            self.s_pullet_group.add(new_pul)
            
        for pos in power_pul:
            new_pul = PPullet(pos)
            self.pullet_group.add(new_pul)
            self.p_pullet_group.add(new_pul)
            
        for pullet in self.pullet_group.sprites():
            pullet.draw(screen)
