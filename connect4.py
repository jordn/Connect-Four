import sys 


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


# print bcolors.WARNING + "Warning: No active frommets remain. Continue?" + bcolors.ENDC

PLAYER_TOKENS = ['X', 'O']

class Board(object):

    def __init__(self, cols=7, rows=6):
        self.cols = cols
        self.rows = rows
        self.grid = [['.']*self.rows for c in xrange(self.cols)]
        self.grid[0][5] = 'R'
        self.player = 1 #whos turn

    def insert(self, column):
        i = len(self.grid[column])-1
        while i >= 0:
            if self.grid[column][i] == '.':
                self.grid[column][i] = PLAYER_TOKENS[self.player]
                self.player = (self.player+1)%2
                break
            i -= 1
        pass

    def check_for_winner(self):
        # vertical
        lines = []
        for column in self.grid:
            lines += ["".join(map(str, column))]
        # horizontal
        for y in range(self.rows):
            lines += ["".join([self.grid[x][y] for x in range(self.cols)])]
        print lines
        # diagonal /
        # diagonal \




    def __str__(self):
        string = '\n'
        for y in range(self.rows):
            string += "  ".join(self.grid[x][y] for x in range(self.cols)) + '\n'
        string += "\n" + "  ".join([str(i) for i in range(self.cols)])
        return string

    def display(self):
        print self

board = Board()

while True:
    print board
    try:
        column = int(raw_input("\nPlayer %s, choose a column: " %PLAYER_TOKENS[board.player]))
    except ValueError:
        print "Please specify a number [0-%i]" % board.cols
    if 0 <= column <= board.cols: 
        board.insert(column)
        board.check_for_winner()

