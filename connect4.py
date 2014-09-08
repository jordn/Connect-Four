#!/usr/bin/env python
# -*- coding: utf-8 -*-

###################
#  CONNECT FOUR   #
#  Jordan Burgess #
#  2014-09-06     #️
#  MIT Licence    #
###################

import sys
import copy
import random

EMPTY = u"⬜"
PLAYER_TOKENS = [u"🔵", u"🔴"]

class Board(object):

    def __init__(self, cols=7, rows=6):
        self.cols = cols
        self.rows = rows
        self.grid = [[EMPTY]*self.rows for c in xrange(self.cols)]
        self.player = 0 # who's turn?

    def insert(self, choice):
        column = choice - 1
        i = len(self.grid[column])-1
        while i >= 0:
            if self.grid[column][i] == EMPTY:
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

    def is_there_a_winner(self):

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

        for line in lines:
            for player in PLAYER_TOKENS:
                if player*4 in line:
                    return player
        return False

    def is_full(self, col=None):
        if col:
            column = self.get_line(col-1, 0, 0, 1)
            if EMPTY in column:
                return False
        else:
            for column in self.grid:
                if EMPTY in column:
                    return False

        return True

    def __unicode__(self):
        string = '\n'
        for y in range(self.rows):
            string += " ".join(self.grid[x][y] for x in range(self.cols)) + '\n'
        string += u" ".join([str(i) for i in range(1, self.cols+1)])
        return string


class Game(object):

    def __init__(self, mode):
        self.board = Board()
        if mode == 1:
            self.ai = AI()

    def play(self):        
        while True:
            print unicode(self.board)

            winner = self.board.is_there_a_winner()
            if winner:
                print "---> %s  Wins!" % winner
                break

            if self.board.is_full():
                print "---> Draw!"
                break

            if (self.board.player == 0 or not hasattr(self, 'ai')):
                try:
                    print u"\nPlayer {0} , choose a column: ".format(PLAYER_TOKENS[self.board.player])
                    col = int(raw_input())
                    if 0 <= col <= self.board.cols and not self.board.is_full(col):
                        self.board.insert(col)
                except ValueError:
                    print "Please specify a number [0-%i]" % self.board.cols
            else:
                self.ai.take_turn(self.board)


class AI(object):

    def take_turn(self, board):

        # Systematically determined to be the optimum Connect-4 strategy
        board.insert(self.evaluate_options(board))

    def evaluate_options(self, board):

        for col in range(1, board.cols+1):
            theoretical_board = copy.deepcopy(board)
            theoretical_board.is_full()
            if theoretical_board.is_full(col):
                continue

            theoretical_board.insert(col)

            print unicode(theoretical_board)

            if theoretical_board.is_there_a_winner():
                print u"\nPlayer {0}  would win in column {1}".format(theoretical_board.is_there_a_winner(), col)
                return col
            else:
                opponent_winning_column = self.evaluate_options(theoretical_board)
                if opponent_winning_column:

                    # Prune off this option
                    return False

        return col


mode = int(raw_input("1 = Single player (against AI)\n2 = 2 player (against friend)\nSELECT MODE:"))
game = Game(mode)
game.play()
