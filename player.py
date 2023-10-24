from board import Board
from ship import Ship
from graphics import render
from input import parseInput, coord_to_coord
import os
from random import randint, choice

class Player:
    def __init__(self, name):
        self.name = name
        self.ships_remaining = 5
        self.ships = {
            '0': Ship('0', 'carrier', 5),
            '1': Ship('1', 'battleship', 4),
            '2': Ship('2', 'cruiser', 3),
            '3': Ship('3', 'submarine', 3),
            '4': Ship('4', 'destroyer', 2)
        }
        self.ship_locations = {}
        self.board = Board()
        self.place_ships()

    def input_coord(self):
        user_input = input("Enter: ")
        coord = parseInput(user_input)
        if coord and self.board.check(coord):
            return coord, [coord_to_coord(coord)]
        else:
            return None, [f'Invalid selection: {user_input}']
        
    def get_ship(self, coord):
        ship_id = self.ship_locations[coord]
        return self.ships[ship_id]

    def receive(self, coord):
        surrender = False
        hit = False
        messages = []
        if coord in self.ship_locations:
            ship = self.get_ship(coord)
            ship.hp -= 1
            hit = True
            messages.append('HIT!')
            if ship.hp == 0:
                messages.append(f'{ship.name} destroyed!')
                self.ships_remaining -= 1
                if self.ships_remaining == 0:
                    messages.append(f'All ships have been destroyed!')
                    messages.append('Game Over')
                    surrender = True
        else:
            messages.append('MISS!')
        return surrender, hit, messages

    def render_board(self, flash):
        os.system('clear')
        print(f'{self.name}')
        print("============")
        self.board.render()
        if flash:
            for msg in flash:
                print(msg)

    def update_board(self, coord, hit):
        if hit:
            self.board.mark(coord, 'O')
        else:
            self.board.mark(coord, 'X')


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