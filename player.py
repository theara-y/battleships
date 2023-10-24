from board import Board
from ship import Ship
from graphics import render
from input import parseInput
import os

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

    def input_coord(self):
        user_input = input("Enter: ")
        coord = parseInput(user_input)
        if coord and self.board.check(coord):
            return coord, []
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