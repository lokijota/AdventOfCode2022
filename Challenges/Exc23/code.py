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
with open('Challenges\Exc23\input.txt') as f:
    lines = f.read().splitlines()

elve_locations = []

for row, line in enumerate(lines):
    for col, map_content in enumerate(line):
        if map_content == '#':
            elve_locations += [(row, col)]

print("Found # elves: ", len(elve_locations))

def print_map(elve_locations):
    # map = np.arange(132).reshape(12,11)
    map = np.full((12,11), ".")
    print(map.shape)

    for elf in elve_locations:
        map[elf[0]+2, elf[1]+2] = '#'

    for row in map:
        for col in row:
            if col == '#':
                print(colored(col, 'red'), end='')
            else:
                print(col, end='')
        print()

# method 4 - hybrid from https://www.geeksforgeeks.org/python-intersection-two-lists/
def intersection(lst1, lst2):
    temp = set(lst2)
    lst3 = [value for value in lst1 if value in temp]
    return lst3
 
# statis definitions helpful to compute coordinates
full_perimeter = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
northwards = [(-1,-1), (-1,0), (-1,1)] # the middle one is the always the direction of movement, if the path is selected
southwards = [(1,-1),  (1,0),  (1,1)]
eastwards =  [(-1,1),  (0,1),  (1,1)]
westwards =  [(-1,-1), (0,-1), (1,-1)]

directions = deque()
directions += [northwards, southwards, westwards, eastwards]

for round in range(1000):

    # first half
    proposed_moves = deque()
    static_elves = set()

    for elf in elve_locations:
        elf_neighbours = [ (elf[0] + p[0], elf[1] + p[1]) for p in full_perimeter]
        if len(intersection(elf_neighbours, elve_locations)) == 0: # feels lonely so it doesn't move
            static_elves.add(elf)
            continue 

        moved = False
        for direction in directions:
            neighbours = [ (elf[0] + p[0], elf[1] + p[1]) for p in direction]
            if len(intersection(neighbours, elve_locations)) > 0:
                continue

            # else propose a move -- (curentpos, newpos) tuple - direction[1] always has the direction of movement
            proposed_move = (elf[0], elf[1], elf[0] + direction[1][0], elf[1] + direction[1][1])
            proposed_moves += [proposed_move]
            moved = True
            break

        if not moved:
            static_elves.add(elf)
    
    # rotate the preferential directions
    old_first_direction = directions.popleft()
    directions += [old_first_direction]

    # second half
    candidate_moving_elves = []

    for proposed_move in proposed_moves:
        matches = [pm for pm in proposed_moves if (pm[2] == proposed_move[2]) and (pm[3] == proposed_move[3])]
        if len(matches) > 1:
            static_elves.add((proposed_move[0], proposed_move[1]))
        else:
            candidate_moving_elves += [(proposed_move[2], proposed_move[3])]

    moving_elves = candidate_moving_elves

    print("Round:", round, ", Moving elves: ", len(moving_elves), ", Static elves: ", len(static_elves), ", total=", len(moving_elves) + len(static_elves))

    if len(moving_elves) == 0:
        print("Round=", round+1)
        break
    # update all the positions now
    elve_locations = moving_elves + list(static_elves)

    # print_map(elve_locations)



# Calculate totals
min_row = 10000
max_row = -10000
min_col = 10000
max_col = -10000

for elf in elve_locations:
    if elf[0] < min_row:
        min_row = elf[0]
    if elf[0] > max_row:
        max_row = elf[0]
    if elf[1] < min_col:
        min_col = elf[1]
    if elf[1] > max_col:
        max_col = elf[1]

# print("Row range: ", min_row, max_row, ", Col range: ", min_col, max_col)

# print("width: ", max_col - min_col + 1, ", height: ", max_row - min_row + 1)
squares = (max_col - min_col + 1) * (max_row - min_row + 1)
# print("Area: ", squares)
print("Score total: ", squares - len(elve_locations))

# 4249 
# part 2 - 980