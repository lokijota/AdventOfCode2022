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
with open('Challenges\Exc22\input.txt') as f:
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

move_north_lambda = lambda coord: (coord[0]-1, coord[1])
move_east_lambda  = lambda coord: (coord[0], coord[1]+1)
move_south_lambda = lambda coord: (coord[0]+1, coord[1])
move_west_lambda  = lambda coord: (coord[0], coord[1]-1)


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
        prev_pos = (start_row, start_col)
        next_pos = (start_row, start_col)
        while steps > 0:
            next_pos = self.next_coordinate(prev_pos[0], prev_pos[1], direction)
            if self.map[next_pos[0]-1][next_pos[1]-1] == "#":
                return prev_pos

            prev_pos = next_pos

            steps -= 1

        return next_pos

    def walkaround(self, candidate_row, candidate_col, direction):
        if direction == DIR_NORTH:
            start_from_row = len(self.map)
            start_from_col = candidate_col
            move_function = move_north_lambda
        elif direction == DIR_EAST:
            start_from_row = candidate_row
            start_from_col = 1
            move_function = move_east_lambda
        elif direction == DIR_WEST :
            start_from_row = candidate_row
            start_from_col = len(self.map[0])
            move_function = move_west_lambda
        else: # SOUTH
            start_from_row = 1
            start_from_col = candidate_col
            move_function = move_south_lambda
        
        # move in the direction until either a # or . is found
        # whats_there = self.map[start_from_row-1][start_from_col-1]
        
        while self.is_offmap((start_from_row, start_from_col)):
            start_from_row, start_from_col = move_function((start_from_row, start_from_col))
        
        whats_there = self.map[start_from_row-1][start_from_col-1]
        while whats_there == " ":
            start_from_row, start_from_col = move_function((start_from_row, start_from_col))
            whats_there = self.map[start_from_row-1][start_from_col-1]

        return (start_from_row, start_from_col)

    def is_offmap(self, pos):
        if pos[0] < 1 or pos[1] < 1 or pos[0] > len(self.map) or pos[1] > len(self.map[pos[0]-1]):
            return True 
        return False

    def next_coordinate(self, row, col, direction):

        # naive implementation, starting point
        if direction == DIR_NORTH:
            candidate_pos = (row - 1, col)
        elif direction == DIR_EAST:
            candidate_pos = (row, col + 1)
        elif direction == DIR_SOUTH:
            candidate_pos = (row + 1, col)
        elif direction == DIR_WEST:
            candidate_pos = (row, col - 1)
        
        # now let's see if there's a wall there, if so we don't move and return immediately
        # this is doe in the previous step - next_pos() function
        # if self.map[candidate_pos[0]-1][candidate_pos[1]-1] == "#":
        #     return (row, col)

        # now let's see if we got off the map -- this is the harder case
        if self.is_offmap(candidate_pos) or self.map[candidate_pos[0]-1][candidate_pos[1]-1] == " ":
            # we need to turn around, and look for either the edge of the map or a space
            candidate_pos = self.walkaround(candidate_pos[0], candidate_pos[1], direction)


        return candidate_pos

    def print(self, player):
        for idxrow, row in enumerate(self.map):
            for idxcol, column in enumerate(row):
                if player.row == idxrow+1 and player.column == idxcol+1:
                    print("X", end="")
                else:
                    print(self.map[idxrow][idxcol], end="")
            print("")    

map = Map(map_rows)
player = PlayerState(1, map.starting_position()[1], DIR_EAST)
player.print()

# map.print(player)

while len(instruction_pairs) > 0:
    command = instruction_pairs.pop()
    steps = int(command[0]) # could do this earlier but this is only done once anyway
    direction = command[1]

    # first try to walk
    next_pos = map.next_pos(player.row, player.column, player.facing, steps)
    player.move(next_pos)

    # map.print(player)

    # then turn
    player.turn(direction)
    print(f"Moved to ({player.row}, {player.column}) and turned {direction} to now face {player.facing}")

print("Final password:", player.row * 1000 + player.column * 4 + (player.facing - 1 ) % 4) 

# 1428