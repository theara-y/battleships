import os
def render(board):
    grid = board.grid
    os.system('clear')
    a = ord("A")
    r = '  '
    for i in range(10):
        r += '  ' + chr(a + i)
    print(r)
    for y in range(len(grid)):
        r = '{: >2}'.format(str(y + 1))
        for x in range(len(grid[y])):
            if grid[y][x] == ' ':
                r += '  □'
            else:
                r += '  ' + '\033[92m' + grid[y][x] + '\033[0m'
        print(r)