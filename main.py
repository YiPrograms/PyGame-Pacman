import pygame

pygame.init()

from env import *
import os
import time

COLOR = [(251, 86, 90), (114, 55, 197), (45, 133, 222), (28, 196, 171), (241, 220, 27)]


def draw_map(file, screen):
    mp = file.read().splitlines()
    vis = set()
    ptx = {}
    pty = {}

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
                ptx.clear()
                pty.clear()
                dfs(i, j)
                for x in ptx.keys():
                    ptx[x].sort()
                    for k in range(0, len(ptx[x]), 2):
                        pygame.draw.line(screen, (0, 0, 255), (x, ptx[x][k]), (x, ptx[x][k+1]), 5)
                for y in pty.keys():
                    pty[y].sort()
                    for k in range(0, len(pty[y]), 2):
                        pygame.draw.line(screen, (0, 0, 255), (pty[y][k], y), (pty[y][k+1], y), 5)

    pygame.display.flip()


def main():
    screen = pygame.display.set_mode((MAP_WIDTH * BLOCK_SIZE, MAP_HEIGHT * BLOCK_SIZE))
    pygame.display.set_caption("Pacman")

    clock = pygame.time.Clock()

    f = open(os.path.join(ASSETS_DIR, "map.txt"), "r")
    draw_map(f, screen)
    f.close()

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()


if __name__ == "__main__":
    while True:
        running = True
        main()
