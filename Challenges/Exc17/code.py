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
    def __init__(self):
        self.board = []
    
    def play_move(self, piece):
        return piece
    
    def height(self):
        return len(self.board)

b = Board()

for i in range(2022):
    b.play_move(piece_generator.next())

print(b.height())