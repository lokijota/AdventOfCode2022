import re
import numpy as np
from operator import itemgetter
import sys
import os
import math
from timeit import default_timer as timer
from tqdm import tqdm
import pickle

sys.path.append(os.path.abspath("."))
print(os.path.abspath("."))
from telegram import *

# ler todas as linhas, como de costume
with open('Challenges\Exc18\input.txt') as f:
    lines = f.read().splitlines()

cubes = [np.array([int(parts) for parts in line.split(",")]) for line in lines]

"""
touching = 0
for cube1 in tqdm(cubes):
    for cube2 in cubes:
        dist = np.linalg.norm(cube2-cube1)
        if dist == 1:
            touching += 1
    
print(touching)
print(len(cubes)*6)
print(len(cubes)*6-touching)
"""

mins = [min([cube[i] for cube in cubes]) for i in range(3)]
maxs = [max([cube[i] for cube in cubes]) for i in range(3)]
# print(mins, maxs) #[1, 0, 0] [19, 19, 19] - cubo 20x20x20
DIM_SIZE = max(maxs) +1


free_positions = [np.array([x,y,z]) for x in range(DIM_SIZE) for y in range(DIM_SIZE) for z in range(DIM_SIZE) if not any(np.array_equal([x,y,z], elem) for elem in cubes)]

with open("Challenges\\Exc18\\free_positions.pkl", "wb") as fp:   #Pickling
    pickle.dump(free_positions, fp)
"""
# Saved to file as it's much faster to load than to generate as above
# with open("Challenges\\Exc18\\free_positions.pkl", "rb") as fp:   # Unpickling
#     free_positions = pickle.load(fp)
"""

# mask of surrounding voxels with contiguous faces, excluding the center
cross_mask = [ [0,1,0], [0,-1,0], [1,0,0], [-1,0,0], [0,0,1], [0,0,-1] ]


def expand_cube(start_pos):
    # print(start_pos)

    mancha = []
    positions_to_check = [start_pos]

    while len(positions_to_check) > 0:

        current_pos = positions_to_check.pop(0)

        # check if the position is occupied
        if not np.any(np.all(current_pos == free_positions, axis=1)):
            continue
        # or if it's already in the mancha
        elif any(np.array_equal(current_pos, elem) for elem in mancha):
            continue

        # position is free and wasn't added yet
        mancha += [current_pos]

        # generate all the positions with touching voxel faces
        touching_positions = [np.array(current_pos) + np.array(pos) for pos in cross_mask]

        # remove positions that are outside the hipercube
        touching_positions = [pos for pos in touching_positions if all([pos[i] >= 0 and pos[i] < DIM_SIZE for i in range(3)])]
        # print(touching_positions)

        # remove positions that are already in the mancha
        touching_positions = [pos for pos in touching_positions if not any(np.array_equal(pos, elem) for elem in mancha)]
        # print(touching_positions)

        # remove positions that are known to be occupied
        touching_positions = [pos for pos in touching_positions if not any(np.array_equal(pos, elem) for elem in cubes)]
        # print(touching_positions)

        positions_to_check += touching_positions
        # print("Positions to check:", len(positions_to_check), ", Mancha:", len(mancha))

    return mancha

print("Expanding cube...")
start = timer()
mancha = expand_cube(np.array([0,0,0]))
end = timer()
print("Done. Time taken:", end-start)

print("total positions: ", DIM_SIZE**3, "contiguous positions:", len(mancha), "all but contiguous:", DIM_SIZE**3-len(mancha), "inside positions:",  DIM_SIZE**3-len(mancha)-len(cubes))

# find the inside position by subtracting the outside positions from the total
print("Finding positions on the inside")
start = timer()
bubbles = [np.array(pos) for pos in free_positions if not any(np.array_equal(pos, elem) for elem in mancha)]
end = timer()
print("Done. Time taken:", end-start)

cubes += bubbles

with open("Challenges\\Exc18\\cubes.pkl", "wb") as fp:   #Pickling
     pickle.dump(cubes, fp)

print("Calculating adjacencies...")
start = timer()

touching = 0
for cube1 in tqdm(cubes):
    for cube2 in cubes:
        dist = np.linalg.norm(cube2-cube1)
        if dist == 1:
            touching += 1

end = timer()
print("Done. Time taken:", end-start)

# print(touching)
# print(len(cubes)*6)
print("Exterior surface area of the lava droplet:", len(cubes)*6-touching)