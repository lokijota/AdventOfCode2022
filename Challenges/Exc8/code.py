# importing numpy library
import numpy as np

# read all the lines
with open('Challenges\Exc8\input.txt') as f:
    # lines = f.readlines() -- not using this as it leaves \n in the strings
    lines = f.read().splitlines()

# put all of this into an bidim array
map = np.array([list(line) for line in lines ], dtype=int)
print(map.shape)

# initialize with the borders
visible_trees = 0 # 99 * 4 - 4 

max_row = map.shape[0]-1
max_col = map.shape[1]-1

for idxrow, row in enumerate(map):
    for idxcol, col in enumerate(row):

        if idxrow == 0 or idxrow == max_row or idxcol == 0 or idxcol == max_col:
            continue

        max_up = max(map[:idxrow,idxcol])
        if max_up < col:
            visible_trees += 1
            continue

        max_down = max(map[idxrow+1:,idxcol])
        if max_down < col:
            visible_trees += 1
            continue

        max_left = max(map[idxrow,:idxcol])
        if max_left < col:
            visible_trees += 1
            continue

        max_right = max(map[idxrow,idxcol+1:])
        if max_right < col:
            visible_trees += 1
            continue

        # print(idxrow, idxcol, max_up)

visible_trees += map.shape[0] * 2 + map.shape[1] * 2 - 4
print(visible_trees)

# 853 too low
# 1948 too high