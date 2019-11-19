from os import path

import pygame
from env import *

DIRECTION = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]


class Pac(pygame.sprite.Sprite):
    def __init__(self, mp, pos, all_sprite, texture="pac.png"):
        super().__init__(all_sprite)
        self.pos = pos
        self.old_pos = pos
        self.speed = 2
        self.block_step = round(BLOCK_SIZE / self.speed)
        self.step = 0
        self.dir = 0
        self.next_dir = 0
        self.on_block = True
        self.image = pygame.image.load(path.join(ASSETS_DIR, texture))
        self.image = pygame.transform.scale(self.image, (BLOCK_SIZE - 8, BLOCK_SIZE - 8))
        self.rect = self.image.get_rect()
        self.map = mp
        self.set_pos(pos)

    def is_road(self, pos):
        return self.map[pos[0]][pos[1]] == " "

    def ch_dir(self, d):
        """
        trying to set new direction for the entity. if there's no way, it would failed and return False.
        :param d:
        :return set successfully or not
        """
        if self.is_road((self.pos[0] + DIRECTION[d][0], self.pos[1] + DIRECTION[d][1])):
            self.next_dir = d
            return True
        return False

    def ch_dir_by_new_xy(self, x, y):
        dx = x - self.get_x()
        dy = y - self.get_y()
        dir_id = 0
        # print("ch dir by xy:", dx, dy)

        for i in range(1, len(DIRECTION)):
            if dx == DIRECTION[i][0] and dy == DIRECTION[i][1]:
                dir_id = i


                break
        return self.ch_dir(dir_id)

    def get_next_pos(self, d):
        x, y = self.pos[0] + DIRECTION[d][0], self.pos[1] + DIRECTION[d][1]
        if y <= -1:
            y = MAP_WIDTH - 1
        elif y >= MAP_WIDTH:
            y = 0
        return x, y

    def set_pos(self, pos):
        self.old_pos = self.pos
        self.pos = pos
        self.rect.centerx = pos[1] * BLOCK_SIZE + BLOCK_SIZE / 2
        self.rect.centery = pos[0] * BLOCK_SIZE + BLOCK_SIZE / 2

    def get_pos(self):
        return self.pos
        # return self.rect.centery // BLOCK_SIZE, self.rect.centerx // BLOCK_SIZE

    def get_old_pos(self):
        return self.old_pos

    def get_x(self):
        return self.pos[0]

    def get_y(self):
        return self.pos[1]

    def get_old_x(self):
        return self.old_pos[0]

    def get_old_y(self):
        return self.old_pos[1]

    def on_destroy(self):
        pass

    def destroy(self):
        self.on_destroy()
        self.kill()

    def update(self):
        # print(self.pos, self.step, self.dir, self.on_block)
        if self.on_block:
            self.step = 0
            if self.next_dir:
                self.dir = self.next_dir
                self.next_dir = 0
                self.on_block = False
            if self.dir:
                if not self.is_road(self.get_next_pos(self.dir)):
                    self.dir = 0
                else:
                    self.pos = self.get_next_pos(self.dir)
                    self.on_block = False

        if self.dir:
            self.rect.centery += DIRECTION[self.dir][0] * self.speed
            self.rect.centerx += DIRECTION[self.dir][1] * self.speed
            self.step += 1
            if self.step >= self.block_step:
                self.on_block = True
                self.set_pos(self.pos)
