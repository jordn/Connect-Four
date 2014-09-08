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
import time

EMPTY = u"⬜"
PLAYER_TOKENS = [u"🔵", u"🔴"]

class Board(object):

    def __init__(self, cols=4, rows=5):
        self.cols = cols
        self.rows = rows
        self.grid = [[EMPTY]*self.rows for c in xrange(self.cols)]
        self.player = 0 # who's turn?

    def insert(self, col):
        i = len(self.grid[col])-1
        while i >= 0:
            if self.grid[col][i] == EMPTY:
                self.grid[col][i] = PLAYER_TOKENS[self.player]
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
            for player in [0,1]:
                if PLAYER_TOKENS[player]*3 in line:
                    return True, player
        return False, None

    def is_full(self, col=None):
        if col:
            column = self.get_line(col, 0, 0, 1)
            if EMPTY in column:
                return False
        else:
            for column in self.grid:
                if EMPTY in column:
                    return False

        return True

    # score from the perspective of player 0
    def evaluate(self):
        winner_exists, player = self.is_there_a_winner()
        print "winner", player
        if winner_exists:
            return 1 if player == 0 else -1
        else:
            return 0

    def current_player(self):
        return PLAYER_TOKENS[self.player]

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

            winner_exists, player = self.board.is_there_a_winner()
            print "winner", player
            if winner_exists:
                print "---> %s  Wins!" % PLAYER_TOKENS[player]
                break

            if self.board.is_full():
                print "---> Draw!"
                break

            if (self.board.player == 0 or not hasattr(self, 'ai')):
                try:
                    print u"\nPlayer {0} , choose a column: ".format(PLAYER_TOKENS[self.board.player])
                    col = int(raw_input()) - 1
                    if 0 <= col <= self.board.cols and not self.board.is_full(col):
                        self.board.insert(col)
                except ValueError:
                    print "Please specify a number [0-%i]" % self.board.cols
            else:
                self.ai.take_turn(self.board)


class AI(object):

    MAX_DEPTH = 3
    def take_turn(self, board):

        # Systematically determined to be the optimum Connect-4 strategy
        choice =self.minimax(board, 1, 0)
        print u"Player {0}  goes in column {1}".format(board.current_player(), choice+1)
        board.insert(choice)

    def minimax(self, board, current_depth, maximising):
        child_scores = []
        for col in range(0, board.cols):
            theoretical_board = copy.deepcopy(board)
            theoretical_board.insert(col)
            # print unicode(theoretical_board)
            time.sleep(0.05)
            if current_depth == self.MAX_DEPTH:
                child_scores.append(theoretical_board.evaluate())
            else:
                child_scores.append(self.minimax(theoretical_board, current_depth+1, (maximising+1%2)))

        print " "*current_depth, child_scores

        if maximising:
            score = max(child_scores)
        else:
            score = min(child_scores)
        index = child_scores.index(score)
        if current_depth == 1: 
            print "Choosing ", index
            return index
        return score

mode = int(raw_input("1 = Single player (against AI)\n2 = 2 player (against friend)\nSELECT MODE:"))
game = Game(mode)
game.play()
