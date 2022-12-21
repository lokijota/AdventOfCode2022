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

# initialize shapes - each tuple is: width, height, sprite as a string
piece_characteristics = {}
piece_characteristics["-"] = (4, 1, "1111")
piece_characteristics["+"] = (3, 3, "010111010")
piece_characteristics["L"] = (3, 3, "001001111")
piece_characteristics["I"] = (1, 4, "1111")
piece_characteristics["o"] = (2, 2, "1111")

print(piece_characteristics)

class Board:
    def __init__(self, gas_generator):
        self.board = ["1111111"] #represent the bottom -- to make tests simpler? Do I also represent the walls? that's silly, however
        self.gas_generator = gas_generator
    
    def play_move(self, piece):

        # prepare for the new move - make 3 rows of space
        self.board.insert(0, "0000000")
        self.board.insert(0, "0000000")
        self.board.insert(0, "0000000")

        # calculate starting pos of piece
        piece_row = self.height() + piece_characteristics[piece][1]
        piece_col = 2

        moved = True
        while moved:
            # the following may return the same position as before, if movement wasn't possible
            piece_row, piece_col, moved_side = self.MoveSideways(gas_generator.next(), piece, piece_row, piece_col)
            piece_row, piece_col, moved_down = self.MoveDown(piece, piece_row, piece_col)

            moved = moved_side or moved_down

        return piece
    
    def MoveSideways(self, direction, piece, row, col):
        return 0, 0, False
    
    def MoveDown(self, piece, row, col):
        return 0, 0, False 
    
    def height(self):
        # this has to be smarter - there may be empty rows at the top after the movement / unless I delete them
        return len(self.board)-1

    def overlap(self, piece, row, col):
        # TBD
        return False

b = Board(gas_generator)

for i in range(2022):
    b.play_move(piece_generator.next())

print(b.height())