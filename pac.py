from os import path

import pygame
from env import *

from search import find_way

class Pac(pygame.sprite.Sprite):
    def __init__(self, mp, pos, all_sprite):
        super().__init__(all_sprite)
        self.mp = mp
        self.pos = pos
        self.speed = 5*60/FPS
        self.block_step = round(BLOCK_SIZE/self.speed)
        self.step = 0
        self.dir = 0
        self.chdir = 0
        self.onblock = True
        self.image = PAC_IMAGE
        self.rect = self.image.get_rect()
        self.set_pos(pos)

    def isroad(self, pos):
        return self.mp[pos[0]][pos[1]] == " "

    def change_dir(self, d):
        if self.isroad((self.pos[0]+DIR[d][0], self.pos[1]+DIR[d][1])):
            self.chdir = d

    def get_dir_pos(self, d):
        x, y = self.pos[0]+DIR[d][0], self.pos[1]+DIR[d][1]
        if y <= -1:
            y = MAP_WIDTH-1
        elif y >= MAP_WIDTH:
            y = 0
        return (x, y)

    def set_pos(self, pos):
        self.pos = pos
        self.rect.centerx = pos[1]*BLOCK_SIZE + BLOCK_SIZE/2
        self.rect.centery = pos[0]*BLOCK_SIZE + BLOCK_SIZE/2
    
    def on_destroy(self):
        pass

    def destroy(self):
        self.on_destroy()
        self.kill()
    
    def update(self):
        if self.onblock:
            self.step = 0
            if self.chdir:
                self.dir = self.chdir
                self.chdir = 0
                self.onblock = False
            if self.dir:
                if not self.isroad(self.get_dir_pos(self.dir)):
                    self.dir = 0
                else:
                    self.pos = self.get_dir_pos(self.dir)
                    self.onblock = False
        
        if self.dir:
            self.rect.centery += DIR[self.dir][0]*self.speed
            self.rect.centerx += DIR[self.dir][1]*self.speed
            self.step += 1
            if self.step >= self.block_step:
                self.onblock = True
                self.set_pos(self.pos)
    
class Ghost(Pac):
    def __init__(self, mp, pos, all_sprite, pac):
        super().__init__(mp, pos, all_sprite)
        self.pac = pac
        self.speed = 2*60/FPS
        self.block_step = round(BLOCK_SIZE/self.speed)
        self.image = RGHOST_IMAGE
        
    def can_turn(self):
        for d in range(len(DIR)):
            if self.isroad((self.pos[0]+DIR[d][0], self.pos[1]+DIR[d][1])):
                return True
        return False
        
    def update(self):
        if self.onblock and self.can_turn():
            d = find_way(self.mp, self.pos, self.pac.pos)
            self.chdir = d
        super().update()

            

