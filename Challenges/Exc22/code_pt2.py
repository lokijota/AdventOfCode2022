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
from termcolor import colored

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

def move_north(coord):
    face = get_face_number(coord[0], coord[1])
    new_coord = (coord[0]-1, coord[1])

    if face == 2 or face == 3 or face == 4:
        return new_coord

    if face == 1 and new_coord[0] == 0: # we hit the edge and go to face 4
        return (100 + new_coord[1], 1)

    if face == 5 and new_coord[0] == 0: # we hit the edge and go to face 4
        return (200, new_coord[1]-100)

    if face == 6 and new_coord[0] == 100: # we hit the edge and go to face 2
        return (50 + new_coord[1],51)
    
    return new_coord

def move_west(coord):
    face = get_face_number(coord[0], coord[1])
    new_coord = (coord[0], coord[1]-1)

    if face == 5 or face == 3:
        return new_coord

    if face == 1 and new_coord[1] == 50: # we hit the edge and go to face 6
        return (150 - new_coord[0] + 1, 1)

    if face == 2 and new_coord[1] == 50: # we hit the edge and go to face 6
        return (101, new_coord[0] - 50)

    if face == 4 and new_coord[1] == 0: # we hit the edge and go to face 1
        return (1, new_coord[0]-100)

    if face == 6 and new_coord[1] == 0: # we hit the edge and go to face 1
        return (150 - new_coord[0] + 1, 51)
    
    return new_coord

def move_east(coord):
    face = get_face_number(coord[0], coord[1])
    new_coord = (coord[0], coord[1]+1)

    if face == 1 or face == 6:
        return new_coord

    if face == 2 and new_coord[1] == 101: # we hit the edge and go to face 5
        return (50, new_coord[0] + 50)

    if face == 3 and new_coord[1] == 101: # we hit the edge and go to face 5
        return (150-new_coord[0]+1,150)

    if face == 4 and new_coord[1] == 51: # we hit the edge and go to face 3
        return (150, new_coord[0]-100)

    if face == 5 and new_coord[1] == 151: # we hit the edge and go to face 3
        return (150-new_coord[0]+1,100)
    
    return new_coord

def move_south(coord):
    face = get_face_number(coord[0], coord[1])
    new_coord = (coord[0]+1, coord[1])

    if face == 1 or face == 2 or face == 6:
        return new_coord

    if face == 3 and new_coord[0] == 151: # we hit the edge and go to face 4
        return (new_coord[1]+100,50)

    if face == 5 and new_coord[0] == 51: # we hit the edge and go to face 2
        return (new_coord[1]-50,100)

    if face == 4 and new_coord[0] == 201: # we hit the edge and go to face 5
        return (1,new_coord[1]+100)
    
    return new_coord

def get_face_number(row, col):
    if row >= 1 and row <= 50 and col >= 50 and col <= 100:
        return 1
    elif row >= 1 and row <= 50 and col >= 101 and col <= 150:
        return 5
    elif row >= 51 and row <= 100 and col >= 51 and col <= 100:
        return 2
    elif row >= 100 and row <= 150 and col >= 1 and col <= 50:
        return 6
    elif row >= 100 and row <= 150 and col >= 51 and col <= 100:
        return 3
    elif row >= 151 and row <= 200 and col >= 1 and col <= 50:
        return 4
    
    print("Error in get_face_number(): row {} col {}".format(row, col))
    assert(False)
    # nota: the above assumes I haven't moved coordinates yet -- falta fazer a transformação de coordenadas

"""
The way to read the following structure is as follows:
if you go from face 1 to face 5, you go east. When you get to face 5, you continue going in DIR_EAST
if you go from face 1 to face 4, you go north. When you get to face 4, you are now going DIR_EAST
What cubes are connected to which ones depend on the numbering scheme I picked and on the dataset. I'm using:
 15
 2
63
4

I constructed a paper cube, with faces numbered as above, to manually construct the following dictionary.
It was sort of boring and error prone. I'm sure there's a better way to do it, but I'm not sure what it is.
"""
direction_translations = {
    # cases where there is no change in directiuon when going across a face
    (1, 5): DIR_EAST,
    (5, 1): DIR_WEST,
    (1, 2): DIR_SOUTH,
    (2, 1): DIR_NORTH,
    (2, 3): DIR_SOUTH,
    (3, 2): DIR_NORTH,
    (6, 3): DIR_EAST,
    (3, 6): DIR_WEST,
    (6, 4): DIR_SOUTH,
    (4, 6): DIR_NORTH,
    (4, 5): DIR_SOUTH,
    (5, 4): DIR_NORTH,
    # cases where there is a change in directiuon when going across a face / this depends on how cube is defined in data input
    (1, 4): DIR_EAST,
    (4, 1): DIR_SOUTH,

    (1, 6): DIR_EAST, 
    (6, 1): DIR_EAST, 

    (2, 5): DIR_NORTH, 
    (5, 2): DIR_WEST, 

    (2, 6): DIR_SOUTH, 
    (6, 2): DIR_EAST, 

    (3, 4): DIR_WEST, 
    (4, 3): DIR_NORTH, 

    (3, 5): DIR_WEST, 
    (5, 3): DIR_WEST
}

# def translate_coordinates(row, col, from_face



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
        print(" > Player is at pos ({},{}), facing direction {} in face # {}".format(self.row, self.column, self.facing, get_face_number(self.row, self.column)))

    def move(self, newpos, direction):
        self.row = newpos[0]
        self.column = newpos[1]
        self.facing = direction

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

    def walk(self, start_row, start_col, direction, steps):
        """
        Calculate the next position, taking in consideration the direction and the number of steps and the game's rules
        """
        prev_pos = (start_row, start_col)
        next_pos = (start_row, start_col)

        # player_marker = 0
        while steps > 0:

            prev_face = get_face_number(prev_pos[0], prev_pos[1])
            next_pos = self.next_coordinate(prev_pos[0], prev_pos[1], direction)
            next_face = get_face_number(next_pos[0], next_pos[1])

            if self.map[next_pos[0]-1][next_pos[1]-1] == "#":
                print(f" > Hit a wall at {next_pos}, stopping")
                return (prev_pos[0], prev_pos[1], direction)

            # DEBUG
            # player_marker = (player_marker + 1) % 10
            # before = self.map[next_pos[0]-1][:next_pos[1]-1]
            # after = self.map[next_pos[0]-1][next_pos[1]:]
            # self.map[next_pos[0]-1] = before + str(player_marker) + after
            # END DEBUG

            prev_pos = next_pos
            if prev_face != next_face:
                new_direction = direction_translations[(prev_face, next_face)]
                if new_direction != direction:
                    print(f"Changed direction from {direction} to {new_direction}")
                    direction = new_direction

            steps -= 1

        return (next_pos[0], next_pos[1], direction)

    def next_coordinate(self, row, col, direction):

        if direction == DIR_NORTH:
            new_pos = move_north((row, col))
        elif direction == DIR_EAST:
            new_pos = move_east((row, col))
        elif direction == DIR_SOUTH:
            new_pos = move_south((row, col))
        elif direction == DIR_WEST:
            new_pos = move_west((row, col))
        
        return new_pos

    def print(self, player):
        for idxrow, row in enumerate(self.map):
            for idxcol, column in enumerate(row):
                if player.row == idxrow+1 and player.column == idxcol+1:
                    if player.facing == DIR_NORTH:
                        print(colored('^', 'red'), end="")
                    elif player.facing == DIR_EAST:
                        print(colored('>', 'red'), end="")
                    elif player.facing == DIR_WEST:
                        print(colored('<', 'red'), end="")
                    elif player.facing == DIR_SOUTH:
                        print(colored('v', 'red'), end="")
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

    print(f"Move forward {steps} steps and then turn {direction}")

    # first try to walk
    row, col, new_direction = map.walk(player.row, player.column, player.facing, steps)
    player.move((row, col), new_direction)

    # map.print(player)

    # then turn
    player.turn(direction)
    player.print()
    # map.print(player)
    # input("(press enter)")
    # print(f" - Moved to ({player.row}, {player.column}) and turned {direction} to now be facing direction {player.facing}")

print("Final password:", player.row * 1000 + player.column * 4 + (player.facing - 1 ) % 4) 

# map.print(player)

# 105111 too low
# 52330... tb seria too low / n vale a pena submeter
# 142380