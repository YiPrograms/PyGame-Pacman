from os import path

import pygame
from env import *

DIR = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]

class Pac(pygame.sprite.Sprite):
    def __init__(self, mp, pos, all_sprite):
        super().__init__(all_sprite)
        self.pos = pos
        self.speed = 5*60/FPS
        self.block_step = round(BLOCK_SIZE/self.speed)
        self.step = 0
        self.dir = 0
        self.chdir = 0
        self.onblock = True
        self.image = pygame.image.load(path.join(ASSETS_DIR, "pac.png"))
        self.image = pygame.transform.scale(self.image, (BLOCK_SIZE-8, BLOCK_SIZE-8))
        self.rect = self.image.get_rect()
        self.mp = mp
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
    
    def get_pos(self):
        return (self.rect.centery//BLOCK_SIZE, self.rect.centerx//BLOCK_SIZE)

    def on_destroy(self):
        pass

    def destroy(self):
        self.on_destroy()
        self.kill()
    
    def update(self):
        print(self.pos, self.step, self.dir, self.onblock)
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
    
            

