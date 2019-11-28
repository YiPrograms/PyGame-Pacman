#! /usr/bin/env python3

import pygame

pygame.init()

from env import *
from sprite import GameSprites
import os
import time

COLOR = [(251, 86, 90), (114, 55, 197), (45, 133, 222), (28, 196, 171), (241, 220, 27)]

ptx = {}
pty = {}

small_pul = []
power_pul = []


def init_map(mp):
    vis = set()

    def dfs(x, y):
        def isempty(x, y):
            if 0 <= x < MAP_HEIGHT and 0 <= y < MAP_WIDTH:
                return mp[x][y] != "#"
            return True

        if (x, y) in vis or isempty(x, y):
            return
        vis.add((x, y))

        def addpt(x, y):
            if not x in ptx.keys():
                ptx[x] = []
            if not y in pty.keys():
                pty[y] = []
            ptx[x].append(y)
            pty[y].append(x)

        if isempty(x - 1, y) and isempty(x, y - 1) or isempty(x - 1, y - 1) and not (
                isempty(x - 1, y) or isempty(x, y - 1)):
            addpt(y * BLOCK_SIZE, x * BLOCK_SIZE)
        if isempty(x + 1, y) and isempty(x, y - 1) or isempty(x + 1, y - 1) and not (
                isempty(x + 1, y) or isempty(x, y - 1)):
            addpt(y * BLOCK_SIZE, (x + 1) * BLOCK_SIZE)
        if isempty(x - 1, y) and isempty(x, y + 1) or isempty(x - 1, y + 1) and not (
                isempty(x - 1, y) or isempty(x, y + 1)):
            addpt((y + 1) * BLOCK_SIZE, x * BLOCK_SIZE)
        if isempty(x + 1, y) and isempty(x, y + 1) or isempty(x + 1, y + 1) and not (
                isempty(x + 1, y) or isempty(x, y + 1)):
            addpt((y + 1) * BLOCK_SIZE, (x + 1) * BLOCK_SIZE)

        dfs(x + 1, y)
        dfs(x - 1, y)
        dfs(x, y + 1)
        dfs(x, y - 1)

    for i in range(MAP_HEIGHT):
        for j in range(MAP_WIDTH):
            if mp[i][j] == "#" and (i, j) not in vis:
                dfs(i, j)
            elif mp[i][j] == " ":
                small_pul.append((i, j))
            elif mp[i][j] == "B":
                power_pul.append((i, j))


def draw_map(screen):
    for x in ptx.keys():
        ptx[x].sort()
        for k in range(0, len(ptx[x]), 2):
            pygame.draw.line(screen, (0, 0, 255), (x, ptx[x][k]), (x, ptx[x][k + 1]), 5)
            pygame.draw.line(screen, (0, 255, 255), (x, ptx[x][k]), (x, ptx[x][k + 1]), 1)
    for y in pty.keys():
        pty[y].sort()
        for k in range(0, len(pty[y]), 2):
            pygame.draw.line(screen, (0, 0, 255), (pty[y][k], y), (pty[y][k + 1], y), 5)
            pygame.draw.line(screen, (0, 255, 255), (pty[y][k], y), (pty[y][k + 1], y), 1)


def main():
    screen = pygame.display.set_mode((MAP_WIDTH * BLOCK_SIZE, MAP_HEIGHT * BLOCK_SIZE))
    pygame.display.set_caption("Pacman")

    global PAC_IMAGE
    global GHOST_EYES
    global GHOST_AFRAID

    PAC_IMAGE.convert()
    GHOST_EYES.convert()
    GHOST_AFRAID.convert()
    for img in GHOST_IMAGES:
        img.convert()

    clock = pygame.time.Clock()
    
    SPLASH_EVENT = pygame.USEREVENT + 1
    SPLASH_TIME = 150
    pygame.time.set_timer(SPLASH_EVENT, SPLASH_TIME)

    f = open(os.path.join(ASSETS_DIR, "map.txt"), "r")
    mp = f.read().splitlines()
    init_map(mp)
    draw_map(screen)
    f.close()

    sp = GameSprites(mp)
    sp.new_pac((15, 9))
    sp.new_ghost((9, 8), 0)
    sp.new_ghost((9, 9), 1)
    sp.new_ghost((9, 10), 2)
    sp.new_ghost((9, 10), 3)
    sp.init_pullets(screen, small_pul, power_pul)
    
    power_mode = False
    power_time = 0

    pygame.display.flip()

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    sp.change_pac_dir(1)
                elif event.key == pygame.K_DOWN:
                    sp.change_pac_dir(2)
                elif event.key == pygame.K_LEFT:
                    sp.change_pac_dir(3)
                elif event.key == pygame.K_RIGHT:
                    sp.change_pac_dir(4)
            if event.type == SPLASH_EVENT:
                sp.splash()
                if power_mode:
                    power_time -= 1

        for ghost in sp.pac_touch_ghost():
            if not ghost.going_home:
                if ghost.afraid:
                    sp.eat_ghost(ghost)
                else:
                    if not sp.get_pac().splash:
                        sp.pac_group.empty()
                        sp.new_pac((15, 9))

        for pullet in sp.eat_small_pullet():
            print("Eat!!!")
            
        for pullet in sp.eat_power_pullet():
            power_time = 80
            power_mode = True
            sp.set_power(True)
                
        if power_mode:
            if power_time == 16:
                sp.power_almost_over()
            elif power_time <= 0:
                power_mode = False
                sp.set_power(False)

        sp.update_all()
        sp.draw_all(screen, [])


if __name__ == "__main__":
    while True:
        running = True
        main()
