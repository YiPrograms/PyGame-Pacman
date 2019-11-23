from queue import PriorityQueue

from env import *


def is_wall(mp, pos, wall):
    if 0 <= pos[0] < MAP_HEIGHT and 0 <= pos[1] < MAP_WIDTH:
        return pos in wall or mp[pos[0]][pos[1]] == "#"
    return True


def a_star(mp, s, e, wall):
    vis = set()
    pq = PriorityQueue()
    pq.put((0, 0, s))
    while not pq.empty():
        _, g, u = pq.get()
        if u in vis:
            continue
        vis.add(u)

        if abs(e[0] - u[0]) + abs(e[1] - u[1]) <= 1:
            return g

        for d in DIR:
            v = (u[0] + d[0], u[1] + d[1])
            if is_wall(mp, v, wall) or v in vis:
                continue

            h = g + 1 + abs(e[0] - v[0]) + abs(e[1] - v[1])
            pq.put((h, g + 1, v))
    return 1e9


def find_way(mp, pos, pac, color):
    res = (1e9, 0)
    wall = [pos]
    e = pac.pos
    if color == 1:
        e = pac.get_dir_pos(pac.dir)
        wall.append(pac.pos)
    elif color == 2:
        e = pac.get_dir_pos(REV_DIR[pac.dir])
        wall.append(pac.pos)

    for d in range(len(DIR)):
        s = (pos[0] + DIR[d][0], pos[1] + DIR[d][1])
        if is_wall(mp, s, []):
            continue

        if s == e:
            return d

        sp = a_star(mp, s, e, wall)
        res = min(res, (sp, d))

    return res[1]
