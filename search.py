import numpy as np
from queue import PriorityQueue
import utils


class Search:
    def __init__(self):
        self.map = np.zeros((30, 30), dtype=np.bool)

    def set_map(self, map_array):
        self.map = map_array

    def update_point(self, x, y, val):
        self.map[x][y] = val

    def _search(self, start, end):
        vis = self.map.copy()
        q = PriorityQueue()
        dx = [0, 0, 1, -1]
        dy = [1, -1, 0, 0]
        for i in range(4):
            new_x = start[0] + dx[i]
            new_y = start[1] + dy[i]
            if not (0 <= new_x < len(self.map) and 0 <= new_y < len(self.map[0])):
                continue
            q.put((utils.mht_distance(new_x, new_y, end[0], end[1]),
                   (new_x, new_y),
                   (new_x, new_y),
                   ))
        while not q.empty():
            obj = q.get()
            x = obj[1][1]
            y = obj[1][1]
            if x == end[0] and y == end[1]:
                return obj[2]
            if vis[x][y]:
                continue
            for i in range(4):
                new_x = start[0] + dx[i]
                new_y = start[1] + dy[i]
                if not (0 <= new_x < len(self.map) and 0 <= new_y < len(self.map[0])):
                    continue
                q.put((obj[0] + 1 + utils.mht_distance(new_x, new_y, end[0], end[1]),
                       (new_x, new_y),
                       obj[2]
                       ))

    def search(self, start, end, update=True):
        x, y = self._search(start, end)
        if update:
            self.map[start[0], start[1]] = False
            self.map[x, y] = True
