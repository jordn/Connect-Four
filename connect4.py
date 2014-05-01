###################
#  CONNECT FOUR   #
#  Jordan Burgess #
#  2014-05-01     #
#  MIT Licence    #
###################


PLAYER_TOKENS = ['X', 'O']

class Board(object):

    def __init__(self, cols=7, rows=6):
        self.cols = cols
        self.rows = rows
        self.grid = [['.']*self.rows for c in xrange(self.cols)]
        self.player = 0 # who's turn?

    def insert(self, column):
        i = len(self.grid[column])-1
        while i >= 0:
            if self.grid[column][i] == '.':
                self.grid[column][i] = PLAYER_TOKENS[self.player]
                self.player = (self.player+1)%2 # Toggle current player
                break
            i -= 1
        pass

    def check_for_winner(self):

        winning_strings = [token * 4 for token in PLAYER_TOKENS]
        print winning_strings
        
        # vertical
        lines = []
        for column in self.grid:
            lines += ["".join(map(str, column))]

        # horizontal
        for y in range(self.rows):
            lines += ["".join([self.grid[x][y] for x in range(self.cols)])]

 
        # diagonal \
        start_x = 0
        for start_y in range(self.rows - 1):
            line = ""
            x, y = start_x, start_y
            while 0 <= x < self.cols and 0 <= y < self.rows:
                line += self.grid[x][y]
                x, y = x+1, y+1
            lines += [line]

        start_y = 0
        for start_x in range(self.cols - 1):
            line = ""
            x, y = start_x, start_y
            while 0 <= x < self.cols and 0 <= y < self.rows:
                line += self.grid[x][y]
                x, y = x+1, y+1
            lines += [line]

        # diagonal /
        start_x = self.cols - 1
        for start_y in range(self.rows - 1):
            line = ""
            x, y = start_x, start_y
            while 0 <= x < self.cols and 0 <= y < self.rows:
                line += self.grid[x][y]
                x, y = x-1, y+1
            lines += [line]

        start_y = self.rows - 1
        for start_x in range(self.cols - 1):
            line = ""
            x, y = start_x, start_y
            while 0 <= x < self.cols and 0 <= y < self.rows:
                line += self.grid[x][y]
                x, y = x+1, y-1
            lines += [line]

        print lines
        # check if a winning string is in lines
        # if winning_strings is in lines
        # print the winner, end the game

    def __str__(self):
        string = '\n'
        for y in range(self.rows):
            string += "  ".join(self.grid[x][y] for x in range(self.cols)) + '\n'
        string += "\n" + "  ".join([str(i) for i in range(self.cols)])
        return string


board = Board()
while True:
    print board
    try:
        column = int(raw_input("\nPlayer %s, choose a column: " %PLAYER_TOKENS[board.player]))
        if 0 <= column <= board.cols: 
            board.insert(column)
            board.check_for_winner()
    except ValueError:
        print "Please specify a number [0-%i]" % board.cols
