from random import randint, choice
from board import Board
from ship import Ship
from player import Player
from input import coord_to_coord
from collections import deque

class Ai(Player):
    def __init__(self, name):
        super().__init__(name)
        self.place_ships()
        self.ships_destroyed = []
        self.shots = deque()
        self.queue_shots = deque()
        self.queue_shots_set = set()

    def place_ships(self):
        self.ship_locations = {}
        self.board = Board()
        for ship in self.ships.values():
            while True:
                coord = self.choose_random_coord()          
                if coord in self.ship_locations:
                    continue
                paths = self.valid_paths(coord, ship.size)
                if paths:
                    path = choice(paths)
                    for path_coord in path:
                        self.ship_locations[path_coord] = ship.id
                        # self.board.mark(path_coord, ship.id)
                    break

    def valid_paths(self, coord, size):
        paths = [
            self.coord_path(coord, [-size, 0]),
            self.coord_path(coord, [size, 0]),
            self.coord_path(coord, [0, size]),
            self.coord_path(coord, [0, -size])
        ]

        good_paths = []
        for path in paths:
            is_valid = True
            for coord in path:
                y, x = coord
                if y < 0 or x < 0 or y > 9 or x > 9 or \
                    coord in self.ship_locations:
                    is_valid = False
                    break
            if is_valid:
                good_paths.append(path)
        return good_paths

    def coord_path(self, coord1, coord2):
        y1, x1 = coord1
        y2, x2 = coord2
        direction = 0
        if y2 < 0 or x2 < 0:
            direction = -1
        elif y2 > 0 or x2 > 0:
            direction = 1
        path = []
        for y in range(y1, y1 + y2 + direction, direction):
            for x in range(x1, x1 + x2 + direction, direction):
                path.append((y, x))
        return path[:-1]

    def choose_random_coord(self):
        return (randint(0, 9), randint(0, 9))
    
    def input_coord(self):
        if len(self.shots) == 0 and len(self.queue_shots) == 0:
        # if True:
            while True:
                coord = self.choose_random_coord()
                if self.board.check(coord):
                    return coord, [coord_to_coord(coord)]
        else:
            if(len(self.shots) == 0):
                self.shots.extend(self.queue_shots.popleft())
            coord = self.shots.popleft()
            return coord, [coord_to_coord(coord)]
            
        

    def update_board(self, coord, hit):
        super().update_board(coord, hit)

        if hit:
            if coord not in self.queue_shots_set:
                y, x = coord
                shots1 = []
                shots2 = []
                shots3 = []
                shots4 = []
                for i in range (1, 5):
                    north = (y - i, x)
                    south = (y + i, x)
                    east = (y, x + i)
                    west = (y, x - i)
                    if self.board.check(north):
                        self.queue_shots_set.add(north)
                        shots1.append(north)
                    if self.board.check(south):
                        self.queue_shots_set.add(south)
                        shots2.append(south)
                    if self.board.check(east):
                        self.queue_shots_set.add(east)
                        shots3.append(east)
                    if self.board.check(west):
                        self.queue_shots_set.add(west)
                        shots4.append(west)

                if len(shots1) != 0:
                    self.queue_shots.append(shots1)
                if len(shots2) != 0:
                    self.queue_shots.append(shots2)
                if len(shots3) != 0:
                    self.queue_shots.append(shots3)
                if len(shots4) != 0:
                    self.queue_shots.append(shots4)
            else:
                self.queue_shots_set.remove(coord)
        else:
            if coord in self.queue_shots_set:
                if len(self.shots) != 0:
                    self.shots.clear()



