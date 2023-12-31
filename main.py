from ai import Ai
from player import Player
import time
import sys

auto = False
if len(sys.argv) > 1 and sys.argv[1] == '--auto':
    auto = True

players = [
    Ai("Player 1"),
    Ai("AI")
]


game_over = False
turns = 0
while not game_over:
    attacking_player = players[turns % len(players)]
    defending_player = players[(turns + 1) % len(players)]
    
    flash = []
    while True:
        attacking_player.render_board(flash)
        coord, messages = attacking_player.input_coord()
        flash.extend(messages)
        if coord:
            response = defending_player.receive(coord)
            game_over = response['game_over']
            flash.extend(response['messages'])
            attacking_player.update_board(coord, response)
            attacking_player.render_board(flash)
            if not auto:
                input("Press Enter to end turn.")
            break

    if not game_over:
        turns += 1

winning_player = players[turns % len(players)]
print(f'{winning_player.name} wins!')

            
        
        