import re
import numpy as np
from operator import itemgetter
import sys
import os
import math
from timeit import default_timer as timer
from tqdm import tqdm
import pickle
from collections import deque

sys.path.append(os.path.abspath("."))
print(os.path.abspath("."))
from telegram import *

# ler todas as linhas, como de costume
with open('Challenges\Exc22\input_debug.txt') as f:
    lines = f.read().splitlines()

map_rows = []
for line in lines:
    if len(line) > 0:
        map_rows += [line]
    else:
        break   

instructions = lines[-1]

# "47L2R45L20L16L2R3"
regex = "(\d+)([LR])?"
instruction_pairs = re.findall(regex, instructions)
instruction_pairs.reverse()

DIR_NORTH = 0
DIR_EAST = 1
DIR_SOUTH = 2
DIR_WEST = 3

class PlayerState:

    def __init__(self, row = 1, column = 1, facing = DIR_EAST):
        self.row = row
        self.column = column # wrong
        self.facing = facing

    def turn(self, direction):
        if direction == 'L':
            self.facing = (self.facing - 1) % 4
        elif direction == 'R':
            self.facing = (self.facing + 1) % 4

        # else don't turn    
        return self.facing

    def print(self):
        print("Play is at row {}, column {}, facing direction {}".format(self.row, self.column, self.facing))

    def move(self, newpos):
        self.row = newpos[0]
        self.column = newpos[1]

class Map:

    def __init__(self, map):
        self.map = map

    def starting_position(self):
        """
        Returns the starting position of the player, in 1-based coordinates, (row, column)
        """
        for col in range(len(self.map[0])):
            if self.map[0][col] == '.':
                return (1, col+1)

        assert(col > 0)

    def next_pos(self, start_row, start_col, direction, steps):
        """
        Calculate the next position, taking in consideration the direction and the number of steps and the game's rules
        """
        # TBD
        return (start_row, start_col)
    
map = Map(map_rows)
player = PlayerState(1, map.starting_position()[1], DIR_EAST)
player.print()

while len(instruction_pairs) > 0:
    command = instruction_pairs.pop()
    steps = command[0]
    direction = command[1]

    # first try to walk
    next_pos = map.next_pos(player.row, player.column, player.facing, steps)
    player.move(next_pos)

    # then turn
    player.turn(direction)
    print(f"Moved to ({player.row}, {player.column}) and turned {direction} to now face {player.facing}")