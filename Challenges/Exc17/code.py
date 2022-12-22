import re
import numpy as np
from operator import itemgetter
import sys
import os
import math
from timeit import default_timer as timer
from tqdm import tqdm

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
        c = self.sequence[self.pointer]
        self.pointer = (self.pointer + 1) % self.size
        return c

gas_generator = Generator(lines[0])
piece_generator = Generator("-+LIo")

# initialize shapes - each tuple is: width, height, sprite as relative coordinates from the top-left corner
piece_characteristics = {}
piece_characteristics["-"] = (4, 1, [(0,0), (0,1), (0,2), (0,3)])
piece_characteristics["+"] = (3, 3, [(0,1), (1,0), (1,1), (1,2), (2,1)])
piece_characteristics["L"] = (3, 3, [(0,2), (1,2), (2,0), (2,1), (2,2)])
piece_characteristics["I"] = (1, 4, [(0,0), (1,0), (2,0), (3,0)])
piece_characteristics["o"] = (2, 2, [(0,0), (0,1), (1,0), (1,1)])

# print(piece_characteristics)

class Board:
    def __init__(self, gas_generator):
        self.board = [] 
        self.gas_generator = gas_generator
    
    def play_move(self, piece):

        # prepare for the new move - make 3 rows of space + height of the piece
        count = 0
        if self.height() >= 1:
            for i in range(7):
                if self.board[i] == "0000000":
                    count += 1
                else:
                    break
        
        if 3 + piece_characteristics[piece][1]-count > 0:
            for i in range(3 + piece_characteristics[piece][1]-count):
                self.board.insert(0, "0000000")
        else: # sigh. for cases with too many rows on the top... can happen if - comes after |
            rows_to_remove = -(3 + piece_characteristics[piece][1]-count)
            for i in range(rows_to_remove):
                self.board.pop(0)

        # calculate starting pos of piece
        piece_row = 0
        piece_col = 2

        moved_down = True
        while moved_down:
            # the following may return the same position as before, if movement wasn't possible
            piece_row, piece_col, _ = self.MoveSideways(gas_generator.next(), piece, piece_row, piece_col)
            piece_row, piece_col, moved_down = self.MoveDown(piece, piece_row, piece_col)

        # Now, put the piece in place on the board

        # calculate new piece coordinates
        where_piece_will_be = [ (c[0] + piece_row, c[1] + piece_col) for c in piece_characteristics[piece][2]]
        
        # now put the piece down
        for c in where_piece_will_be:
            self.board[c[0]] = self.board[c[0]][:c[1]] + "#" + self.board[c[0]][c[1]+1:]

            # self.board[c[0]][c[1]] = piece

        # remove empty rows from the top -- this can be optimized/avoided...
        # while self.board[0] == "0000000":
        #     self.board.pop(0)

        return piece
    
    def MoveSideways(self, direction, piece, row, col):
        if direction == "<": # left
            if col-1 < 0:
                return row, col, False

            if self.overlap(piece, row, col-1):
                return row, col, False

            return row, col-1, True

        else: # right
            if col + piece_characteristics[piece][0] > 6:
                return row, col, False

            if self.overlap(piece, row, col+1):
                return row, col, False

            return row, col+1, True

    def MoveDown(self, piece, row, col):

        # if the piece is already at the bottom, it can't move down
        # remember that row 0 is the topmost one
        if row + piece_characteristics[piece][1] >= self.height():
            return row, col, False

        if self.overlap(piece, row+1, col):
            return row, col, False

        return row+1, col, True 
    
    def height(self):
        # this has to be smarter - there may be empty rows at the top after the movement / unless I delete them
        return len(self.board)

    def true_height(self):
        
        # count empty rows at top just with 0000000
        count = 0
        if self.height() > 0:
            for i in range(7):
                if self.board[i] == "0000000":
                    count += 1
                else:
                    break

        return self.height() - count

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

"""
for i in range(2022): 
    b.play_move(piece_generator.next())
    # b.print_board()
    # print()

print(b.true_height())
# part 1 - 3159
exit()
"""


STABILIZE_DELTA = 200
CYCLE_LENGHT = 1690 # the results start repeating in blocks of 1690 rows (in terms of height increases)
for i in tqdm(range(STABILIZE_DELTA)): 
    b.play_move(piece_generator.next())

running_height = b.true_height()

heights = [0]

for i in tqdm(range(CYCLE_LENGHT)):
    b.play_move(piece_generator.next())
    heights += [b.true_height() - running_height - sum(heights)] 

heights.pop(0)

print("Sum of first 200 is", running_height)
print("Sum of each 1670 is", sum(heights))
print("How many times 1670 fits into the 1B - STABILIZE_DELTA is", math.floor((1000000000000-STABILIZE_DELTA)/CYCLE_LENGHT))
running_height += math.floor((1000000000000-STABILIZE_DELTA)/CYCLE_LENGHT) * sum(heights)

print("# records processed", STABILIZE_DELTA + math.floor((1000000000000-STABILIZE_DELTA)/CYCLE_LENGHT)*CYCLE_LENGHT)

records_to_process = 1000000000000 - STABILIZE_DELTA - math.floor((1000000000000-STABILIZE_DELTA)/CYCLE_LENGHT)*CYCLE_LENGHT
print("Records to add", records_to_process)

running_height += sum(heights[:records_to_process])

print("Estimated submission is", running_height)

# part 2 - 1566272189352

