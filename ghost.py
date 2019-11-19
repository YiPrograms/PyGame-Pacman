from pac import Pac


class Ghost(Pac):
    def __init__(self, mp, pos, all_sprite, texture="blinky.png"):
        super().__init__(mp, pos, all_sprite, texture)

    def is_road(self, pos):
        return self.map[pos[0]][pos[1]] != "#"
