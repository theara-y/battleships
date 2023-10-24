from ai import Ai
import time
import sys

auto = False
if len(sys.argv) > 1 and sys.argv[1] == '--auto':
    auto = True

def get_input(player):
    if auto:
        coord = player.choose_random_coord()
        valid = player.board.check(coord)
        return coord, valid, []
    else:
        coord, flash = player.input_coord()
        return coord, True, flash


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
        coord, valid, flash = get_input(attacking_player)
        if coord and valid:
            game_over, hit, flash = defending_player.receive(coord)
            attacking_player.update_board(coord, hit)
            attacking_player.render_board(flash)
            if not auto:
                input("Press Enter to end turn.")
            # time.sleep(1)
            break

    if not game_over:
        turns += 1

winning_player = players[turns % len(players)]
print(f'{winning_player.name} wins!')

            
        
        