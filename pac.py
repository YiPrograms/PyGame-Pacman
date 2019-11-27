from os import path

import pygame
from env import *

from search import find_way, a_star_trace


class Pac(pygame.sprite.Sprite):
    def __init__(self, mp, pos):
        super().__init__()
        self.mp = mp
        self.pos = pos
        self.speed = 3 * 60 / FPS
        self.block_step = round(BLOCK_SIZE / self.speed)
        self.step = 0
        self.dir = 0
        self.chdir = 0
        self.onblock = True
        self.image = self.org_img = PAC_IMAGE
        self.rect = self.image.get_rect()
        self.splash = 16
        self.set_pos(pos)

    def isroad(self, pos):
        if 0 <= pos[0] < MAP_HEIGHT and 0 <= pos[1] < MAP_WIDTH:
            return self.mp[pos[0]][pos[1]] != "#" and self.mp[pos[0]][pos[1]] != "X"
        return False
    
    def set_speed(self, speed):
        self.speed = speed * 60 / FPS
        self.block_step = round(BLOCK_SIZE / self.speed)

    def change_dir(self, d):
        if self.isroad((self.pos[0] + DIR[d][0], self.pos[1] + DIR[d][1])):
            self.chdir = d

    def get_dir_pos(self, d):
        x, y = self.pos[0] + DIR[d][0], self.pos[1] + DIR[d][1]
        if y <= -1:
            y = MAP_WIDTH - 1
        elif y >= MAP_WIDTH:
            y = 0
        return (x, y)

    def set_pos(self, pos):
        self.pos = pos
        self.rect.centerx = pos[1] * BLOCK_SIZE + BLOCK_SIZE / 2
        self.rect.centery = pos[0] * BLOCK_SIZE + BLOCK_SIZE / 2

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
            self.rect.centery += DIR[self.dir][0] * self.speed
            self.rect.centerx += DIR[self.dir][1] * self.speed
            self.step += 1
            if self.step >= self.block_step:
                self.onblock = True
                self.set_pos(self.pos)


class Ghost(Pac):
    def __init__(self, mp, pos, pac, color):
        super().__init__(mp, pos)
        self.color = color
        self.pac = pac
        self.speed = 3 * 60 / FPS
        self.block_step = round(BLOCK_SIZE / self.speed)
        self.image = GHOST_IMAGES[self.color]
        self.org_img = GHOST_AFRAID
        self.splash = 0
        self.afraid = False
        self.going_home = False
        self.home_path = []
        self.home_id = 0

    def isroad(self, pos):
        if 0 <= pos[0] < MAP_HEIGHT and 0 <= pos[1] < MAP_WIDTH:
            return self.mp[pos[0]][pos[1]] != "#"
        return False

    def update(self):
        if self.onblock:
            if self.going_home:
                if self.home_id < 0:
                    self.going_home = False
                    self.image = GHOST_IMAGES[self.color]
                    self.set_speed(3)
                else:
                    next_pos = self.home_path[self.home_id]
                    self.home_id -= 1
                    d = (next_pos[0] - self.pos[0], next_pos[1] - self.pos[1])
                    self.chdir = DIR.index(d)   
            else:
                d = find_way(self.mp, self.pos, self.pac.sprites()[0], self.color, self.afraid)
                self.chdir = d
                
        super().update()
    
    def go_home(self):
        self.image = GHOST_EYES
        self.afraid = False
        self.going_home = True
        self.splash = 0
        self.home_path.clear()
        trace = a_star_trace(self.mp, self.pos, (9, 9))
        cur = (9, 9)
        self.home_path.append(cur)
        while trace[cur] != -1:
            cur = trace[cur]
            self.home_path.append(cur)
        self.home_id = len(self.home_path)-2
        self.set_speed(10)
        

