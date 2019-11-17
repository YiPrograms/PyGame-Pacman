import pygame

pygame.init()

from env import *
import os
import time

COLOR = [(251, 86, 90), (114, 55, 197), (45, 133, 222), (28, 196, 171), (241, 220, 27)]


def draw_map(file, screen):
    mp = file.read().splitlines()
    vis = set()
    blk = None
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
            if x not in ptx.keys():
                ptx[x] = []
            if y not in pty.keys():
                pty[y] = []
            ptx[x].append(y)
            ptx[y].append(x)

        #blk = (pygame.Rect(y*BLOCK_SIZE, x*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        #pygame.draw.rect(screen, COLOR[colorid % 4], blk)

        if isempty(x-1, y) and isempty(x, y-1) or isempty(x-1, y-1) and not(isempty(x-1, y) or isempty(x, y-1)):
            addpt(y*BLOCK_SIZE, x*BLOCK_SIZE)
        if isempty(x+1, y) and isempty(x, y-1) or isempty(x+1, y-1) and not(isempty(x+1, y) or isempty(x, y-1)):
            addpt(y*BLOCK_SIZE, (x+1)*BLOCK_SIZE)
        if isempty(x-1, y) and isempty(x, y+1) or isempty(x-1, y+1) and not(isempty(x-1, y) or isempty(x, y+1)):
            addpt((y+1)*BLOCK_SIZE, x*BLOCK_SIZE)
        if isempty(x+1, y) and isempty(x, y+1) or isempty(x+1, y+1) and not(isempty(x+1, y) or isempty(x, y+1)):
            addpt((y+1)*BLOCK_SIZE, (x+1)*BLOCK_SIZE)

        #pygame.display.flip()
        #time.sleep(0.5)

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
                pygame.display.flip()
                return
                #colorid += 1
                
            # if mp[i][j] == "#":
            #     pygame.draw.rect(screen, (0, 255, 255), pygame.Rect(j*BLOCK_SIZE, i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 2)

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
