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

road = []

def init_map(mp):
    vis = set()

    def dfs(x, y):
        def isempty(x, y):
            if 0 <= x < MAP_HEIGHT and 0 <= y < MAP_WIDTH:
                return mp[x][y] == " "
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

        if isempty(x-1, y) and isempty(x, y-1) or isempty(x-1, y-1) and not(isempty(x-1, y) or isempty(x, y-1)):
            addpt(y*BLOCK_SIZE, x*BLOCK_SIZE)
        if isempty(x+1, y) and isempty(x, y-1) or isempty(x+1, y-1) and not(isempty(x+1, y) or isempty(x, y-1)):
            addpt(y*BLOCK_SIZE, (x+1)*BLOCK_SIZE)
        if isempty(x-1, y) and isempty(x, y+1) or isempty(x-1, y+1) and not(isempty(x-1, y) or isempty(x, y+1)):
            addpt((y+1)*BLOCK_SIZE, x*BLOCK_SIZE)
        if isempty(x+1, y) and isempty(x, y+1) or isempty(x+1, y+1) and not(isempty(x+1, y) or isempty(x, y+1)):
            addpt((y+1)*BLOCK_SIZE, (x+1)*BLOCK_SIZE)

        dfs(x+1, y)
        dfs(x-1, y)
        dfs(x, y+1)
        dfs(x, y-1)

    for i in range(MAP_HEIGHT):
        for j in range(MAP_WIDTH):
            if (i, j) not in vis and mp[i][j] != " ":
                dfs(i, j)

    for i in range(MAP_HEIGHT):
        for j in range(MAP_WIDTH):
            if (i, j) not in vis:
                road.append((i, j))
        
def draw_map(screen):
    for x in ptx.keys():
        ptx[x].sort()
        for k in range(0, len(ptx[x]), 2):
            pygame.draw.line(screen, (0, 0, 255), (x, ptx[x][k]), (x, ptx[x][k+1]), 5)
            pygame.draw.line(screen, (0, 255, 255), (x, ptx[x][k]), (x, ptx[x][k+1]), 1)
    for y in pty.keys():
        pty[y].sort()
        for k in range(0, len(pty[y]), 2):
            pygame.draw.line(screen, (0, 0, 255), (pty[y][k], y), (pty[y][k+1], y), 5)
            pygame.draw.line(screen, (0, 255, 255), (pty[y][k], y), (pty[y][k+1], y), 1)

    


def main():
    screen = pygame.display.set_mode((MAP_WIDTH * BLOCK_SIZE, MAP_HEIGHT * BLOCK_SIZE))
    pygame.display.set_caption("Pacman")

    clock = pygame.time.Clock()

    f = open(os.path.join(ASSETS_DIR, "map.txt"), "r")
    mp = f.read().splitlines()
    init_map(mp)
    draw_map(screen)
    f.close()
    
    sp = GameSprites(mp)
    sp.new_pac((15, 9))
    sp.new_ghost((9, 8), 1)
    sp.new_ghost((9, 9), 2)
    sp.new_ghost((9, 10), 3)
    sp.init_pullets(screen, road)

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
                elif event.key == pygame.K_SPACE:
                    sp.new_pac((15, 9))

        for ghost in  sp.pac_touch_ghost():
            sp.pac_group.empty()
            
        
        for pullet in sp.eat_pullet():
            print("Eat!!!")

        sp.update_all()
        sp.draw_all(screen, [])



if __name__ == "__main__":
    while True:
        running = True
        main()
