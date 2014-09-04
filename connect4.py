###################
#  CONNECT FOUR   #
#  Jordan Burgess #
#  2014-05-01     #
#  MIT Licence    #
###################

import sys

BLUE = '\033[94m'
RED = '\033[91m'
END_COLOR = '\033[0m'
PLAYER_TOKENS = [RED+'X'+END_COLOR, BLUE+'O'+END_COLOR]

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


    def get_line(self, start_x, start_y, delta_x, delta_y):
        line = ""
        x, y = start_x, start_y
        while 0 <= x < self.cols and 0 <= y < self.rows:
            line += self.grid[x][y]
            x, y = x+delta_x, y+delta_y
        return line


    def check_for_winner(self):

        lines = []
        # vertical 
        lines += [self.get_line(x, 0, 0, 1) for x in range(self.cols)]
        # horizontal
        lines += [self.get_line(0, y, 1, 0) for y in range(self.rows)]
        # diagonal \
        lines += [self.get_line(0, y, 1, 1) for y in range(self.rows-1)]
        lines += [self.get_line(x, 0, 1, 1) for x in range(self.cols-1)]
        # diagonal /
        lines += [self.get_line(self.cols-1, y, -1, 1) for y in range(self.rows-1)]
        lines += [self.get_line(x, self.rows-1, 1, -1) for x in range(self.cols-1)]

        last_player = PLAYER_TOKENS[(self.player+1)%2]

        for line in lines:
            if last_player*4 in line:
                print "---> %s Wins!" % last_player
                sys.exit()

    def __str__(self):
        string = '\n'
        for y in range(self.rows):
            string += "  ".join(self.grid[x][y] for x in range(self.cols)) + '\n'
        string += "\n" + "  ".join([str(i) for i in range(self.cols)])
        return string


class Game(object):

    def __init__(self):
        self.board = Board()

    def play(self):        
        while True:
            print self.board
            try:
                column = int(raw_input("\nPlayer %s, choose a column: " % PLAYER_TOKENS[self.board.player]))
                if 0 <= column < self.board.cols: self.board.insert(column)
            except ValueError:
                print "Please specify a number [0-%i]" % self.board.cols

            self.board.check_for_winner()


game = Game()
game.play()