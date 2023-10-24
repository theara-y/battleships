class Board:
    def __init__(self):
        self.checked = set()
        self.grid = [[' ' for i in range(10)] for j in range(10)]

    def mark(self, coord, char):
        self.grid[coord[0]][coord[1]] = char
        self.checked.add(coord)

    def check(self, coord):
        if coord in self.checked:
            return False
        return True
    
    def place(self, path, char):
        for coord in path:
            y, x = coord
            self.grid[y][x] = char

    def render(self):
        a = ord("A")
        r = '  '
        for i in range(10):
            r += '  ' + chr(a + i)
        print(r)
        for y in range(len(self.grid)):
            r = '{: >2}'.format(str(y + 1))
            for x in range(len(self.grid[y])):
                if self.grid[y][x] == ' ':
                    r += '  □'
                elif self.grid[y][x] == 'X':
                    r += '  ' + '\033[91m' + self.grid[y][x] + '\033[0m'
                else:
                    r += '  ' + '\033[92m' + self.grid[y][x] + '\033[0m'
            print(r)

