from queue import PriorityQueue

from env import *
from random import randint


def is_wall(mp, pos, wall):
    if 0 <= pos[0] < MAP_HEIGHT and 0 <= pos[1] < MAP_WIDTH:
        return pos in wall or mp[pos[0]][pos[1]] == "#"
    return True


def a_star(mp, pos, e, wall):
    vis = set()
    pq = PriorityQueue()
    
    for d in range(len(DIR)):
        s = (pos[0] + DIR[d][0], pos[1] + DIR[d][1])
        if is_wall(mp, s, []):
            continue
        if s == e:
            return d
        pq.put((0, 0, s, d))
    
    while not pq.empty():
        _, g, u, ud = pq.get()
        if u in vis:
            continue
        vis.add(u)

        if abs(e[0] - u[0]) + abs(e[1] - u[1]) <= 2:
            return ud

        for d in DIR:
            v = (u[0] + d[0], u[1] + d[1])
            if is_wall(mp, v, wall) or v in vis:
                continue

            h = g + 1 + abs(e[0] - v[0]) + abs(e[1] - v[1])
            pq.put((h, g + 1, v, ud))
    return 0

def a_star_trace(mp, s, e):
    vis = set()
    pq = PriorityQueue()
    trace = {}
    
    pq.put((0, 0, s, -1))
    
    while not pq.empty():
        _, g, u, f = pq.get()
        if u in vis:
            continue
        vis.add(u)
        trace[u] = f

        if u==e:
            return trace

        for d in DIR:
            v = (u[0] + d[0], u[1] + d[1])
            if is_wall(mp, v, []) or v in vis:
                continue

            h = g + 1 + abs(e[0] - v[0]) + abs(e[1] - v[1])
            pq.put((h, g + 1, v, u))
    return -1


def find_way(mp, pos, pac, color, afraid):
    wall = [pos]
    e = pac.pos
    if color == 1:
        e = pac.get_dir_pos(pac.dir)
        wall.append(pac.pos)
    elif color == 2:
        e = pac.get_dir_pos(REV_DIR[pac.dir])
        wall.append(pac.pos)
    elif color == 3:
        e = pac.get_dir_pos(randint(0, 3))
        wall.append(pac.pos)
    
    if afraid:
        e = (MAP_HEIGHT-1-e[0], MAP_WIDTH-1-e[1])
    

    return a_star(mp, pos, e, wall)
