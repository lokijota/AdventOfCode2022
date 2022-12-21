import re
import numpy as np
from operator import itemgetter
import sys
import os
import math
from timeit import default_timer as timer

sys.path.append(os.path.abspath("."))
print(os.path.abspath("."))
from telegram import *

# ler todas as linhas, como de costume
with open('Challenges\Exc17\input.txt') as f:
    lines = f.read().splitlines()

class Generator:
    def __init__(self, sequence):
        self.sequence = sequence
        self.pointer = 0
        self.size = len(sequence)

    def next(self):
        self.pointer = (self.pointer + 1) % self.size
        return self.sequence[self.pointer]

gas_generator = Generator(lines[0])
piece_generator = Generator("-+LIo")

# initialize shapes - each tuple is: width, height, sprite as relative coordinates from the top-left corner
piece_characteristics = {}
piece_characteristics["-"] = (4, 1, [(0,0), (0,1), (0,2), (0,3)])
piece_characteristics["+"] = (3, 3, [(0,1), (1,0), (1,1), (1,2), (2,1)])
piece_characteristics["L"] = (3, 3, [(0,2), (1,2), (2,0), (2,1), (2,2)])
piece_characteristics["I"] = (1, 4, [(0,0), (1,0), (2,0), (3,0)])
piece_characteristics["o"] = (2, 2, [(0,0), (0,1), (1,0), (1,1)])

print(piece_characteristics)

class Board:
    def __init__(self, gas_generator):
        self.board = ["1111111"] #represent the bottom -- to make tests simpler? Do I also represent the walls? that's silly, however
        self.gas_generator = gas_generator
    
    def play_move(self, piece):

        # prepare for the new move - make 3 rows of space + height of the piece
        for i in range(3 + piece_characteristics[piece][1]):
            self.board.insert(0, "0000000")

        # calculate starting pos of piece
        piece_row = self.height()
        piece_col = 2

        moved = True
        while moved:
            # the following may return the same position as before, if movement wasn't possible
            piece_row, piece_col, moved_side = self.MoveSideways(gas_generator.next(), piece, piece_row, piece_col)
            piece_row, piece_col, moved_down = self.MoveDown(piece, piece_row, piece_col)

            moved = moved_side or moved_down

        # JOTA: DO SOMETHING -- PUT THE PIECE IN PLACE ON THE BOARD

        while self.board[0] == "0000000":
            self.board.pop(0)

        return piece
    
    def MoveSideways(self, direction, piece, row, col):
        if direction == "<": # left
            if col-1 < 0:
                return row, col, False

            if self.overlap(piece, row, col-1):
                return row, col, False

            return row, col-1, True

        else: # right
            if col + 1 + piece_characteristics[piece][0] > 6:
                return row, col, False

            if self.overlap(piece, row, col+1):
                return row, col, False

            return row, col+1, True

    def MoveDown(self, piece, row, col):

        # if the piece is already at the bottom, it can't move down
        if row - piece_characteristics[piece][1] < 0:
            return row, col, False

        if self.overlap(piece, row-1, col):
            return row, col, False

        return row-1, col, True 
    
    def height(self):
        # this has to be smarter - there may be empty rows at the top after the movement / unless I delete them
        return len(self.board)-1

    def overlap(self, piece, row, col):
        # check if the piece overlaps with existing pieces on the board
        
        # calculate new piece coordinates
        where_piece_will_be = [ (c[0] + row, c[1] + col) for c in piece_characteristics[piece][2]]
        
        # now check what's on the board in this position 
        for c in where_piece_will_be:
            if self.board[c[0]][c[1]] != "0":
                return True

        return False

    def print_board(self):
        for i in range(len(self.board)):
            print(self.board[i])


b = Board(gas_generator)

for i in range(2022):
    b.play_move(piece_generator.next())
    b.print_board()

print(b.height())