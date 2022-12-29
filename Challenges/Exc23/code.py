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

# map_rows = []
# for line in lines:
#     if len(line) > 0:
#         map_rows += [line]
#     else:
#         break   

elve_locations = []

for row, line in enumerate(lines):
    for col, map_content in enumerate(line):
        if map_content == '#':
            elve_locations += [(row, col)]

print("Found # elves: ", len(elve_locations))

# method 4 - hybrid from https://www.geeksforgeeks.org/python-intersection-two-lists/
def intersection(lst1, lst2):
    temp = set(lst2)
    lst3 = [value for value in lst1 if value in temp]
    return lst3
 
# # Driver Code
# lst1 = [9, 9, 74, 21, 45, 11, 63]
# lst2 = [4, 9, 1, 17, 11, 26, 28, 28, 26, 66, 91]
# print(intersection(lst1, lst2))

full_perimeter = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

northwards = [(-1,-1), (-1,0), (-1,1),  (-1,0)] # last is always the direction of movement / same as the middle one but meh
southwards = [(1,-1),  (1,0),  (1,1),   (1,0)]
eastwards =  [(-1,1),  (0,1),  (1,1),   (0,1)]
westwards =  [(-1,-1), (0,-1), (1,-1),  (0,-1)]

directions = deque()
directions += [northwards, southwards, eastwards, westwards]

for round in range(10):

    # first half
    proposed_moves = deque()
    static_elves = set()

    for elf in elve_locations:
        elf_neighbours = [ (elf[0] + p[0], elf[1] + + p[1]) for p in full_perimeter]
        if len(intersection(elf_neighbours, elve_locations)) == 0:
            static_elves.add(elf)
            continue # next elf

        moved = False
        for direction in directions:
            neighbours = [ (elf[0] + p[0], elf[1] + p[1]) for p in direction[:3]]
            if len(intersection(neighbours, elve_locations)) > 0:
                continue

            # else propose a move -- (curentpos, newpos) tuple 
            proposed_move = (elf[0], elf[1], elf[0] + direction[3][0], elf[1] + direction[3][1])
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

    # (3,2) está nas duas! como é possível??
    for proposed_move in proposed_moves:
        matches = [pm for pm in proposed_moves if pm[2] == proposed_move[2] and pm[3] == proposed_move[3]]
        if len(matches) > 1:
            # print("  more than one elves want to move to the same position, none will move", matches)
            static_elves.add((proposed_move[0], proposed_move[1]))
        elif (proposed_move[2], proposed_move[3]) in static_elves:
            static_elves.add((proposed_move[0], proposed_move[1]))
        else:
            # print("  found elf to move")
            candidate_moving_elves += [proposed_move]

    moving_elves = []
    for candidate_moving_elf in candidate_moving_elves:
        if (candidate_moving_elf[2], candidate_moving_elf[3]) in static_elves:
            static_elves.add((candidate_moving_elf[0], candidate_moving_elf[1]))
        else:
            moving_elves += [(candidate_moving_elf[2], candidate_moving_elf[3])]

    print("Moving elves: ", len(moving_elves), ", Static elves: ", len(static_elves), ", total=", len(moving_elves) + len(static_elves))

    # update all the positions now
    elve_locations = moving_elves + list(static_elves)

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

print("width: ", max_col - min_col + 1, ", height: ", max_row - min_row + 1)
squares = (max_col - min_col + 1) * (max_row - min_row + 1)
print("Area: ", squares)
print("Score total: ", squares - len(elve_locations))

# 4333 is too high
# 4249 OK / no entanto não funciona para o debug dataset, falta uma coluna!