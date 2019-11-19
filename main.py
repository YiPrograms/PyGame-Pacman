#! /usr/bin/env python3

import pygame

import pac
from ghost import Ghost
from search import Search

pygame.init()

from env import *
from pac import Pac
import os
import time

COLOR = [(251, 86, 90), (114, 55, 197), (45, 133, 222), (28, 196, 171), (241, 220, 27)]

ptx = {}
pty = {}


def create_map(mp):
    """
    add things to ptx & pty. only use when initialize the map.
    :param mp:
    :return: None
    """
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
            if x not in ptx.keys():
                ptx[x] = []
            if y not in pty.keys():
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
            if (i, j) not in vis and mp[i][j] != " ":
                dfs(i, j)


def draw_map(screen):
    """
    only use when initialize the map.
    :param screen:
    :return:
    """

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

    clock = pygame.time.Clock()

    with open(os.path.join(ASSETS_DIR, "map.txt"), "r") as f:
        pacman_map = f.read().splitlines()
        create_map(pacman_map)
    all_sprite = pygame.sprite.Group()
    player = Pac(pacman_map, (15, 9), all_sprite)

    ghost_blinky = Ghost(pacman_map, (10, 8), all_sprite, texture="blinky.png")
    ghost_pinky = Ghost(pacman_map, (10, 8), all_sprite, texture="pinky.png")
    # ghost_inky = Ghost(pacman_map, (15, 9), all_sprite)
    # ghost_clyde = Ghost(pacman_map, (15, 9), all_sprite)

    search = Search().set_map(pacman_map)
    print(search.map)
    all_sprite.draw(screen)
    pygame.display.flip()

    while running:
        clock.tick(FPS)
        all_sprite.update()
        screen.fill((0, 0, 0))
        draw_map(screen)
        all_sprite.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.ch_dir(1)
                elif event.key == pygame.K_DOWN:
                    player.ch_dir(2)
                elif event.key == pygame.K_LEFT:
                    player.ch_dir(3)
                elif event.key == pygame.K_RIGHT:
                    player.ch_dir(4)
        pygame.display.flip()

        # TODO: Update Ghost's target
        # player also known as wall to the ghosts 'cos they can't go through the player,
        # But they can cross the other ghosts.
        player_old_pos = player.get_old_pos()
        player_pos = player.get_pos()
        """
        Blinky will simply trace the player in the shortest way.
        pinky will aim to 2 blocks in front of player.
        the AI of Inky is complicated. first, let Point A = the point which 2 block in front of player.
        Then draw line from Blinky to A, extending double length, the position is the target that Inky is aiming to. 
        """
        b_x, b_y = search.search(ghost_pinky.get_pos(), player_pos)
        ghost_blinky.ch_dir_by_new_xy(b_x, b_y)
        # get the target of pinky
        pinky_target = (0, 0)
        for i in range(3):
            if ghost_pinky.is_road(player.get_next_pos(i)):
                pinky_target = player.get_next_pos(i)

        p_x, p_y = search.search(ghost_pinky.get_pos(), pinky_target)
        ghost_pinky.ch_dir_by_new_xy(p_x, p_y)

        search.update_point(player_old_pos[0], player_old_pos[1], False)
        search.update_point(player_pos[0], player_pos[1], True)



if __name__ == "__main__":
    while True:
        running = True
        main()
