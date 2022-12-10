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
max_scenic_score = 0

max_row = map.shape[0]-1
max_col = map.shape[1]-1

def how_many_do_i_see(tree_height, trees_in_range):
    count = 0
    for tree in trees_in_range:
        if tree >= tree_height:
            return count+1
        count += 1 
    return count

for idxrow, row in enumerate(map):
    for idxcol, current_tree_height in enumerate(row):

        if idxrow == 0 or idxrow == max_row or idxcol == 0 or idxcol == max_col:
            continue

        tree_scenic_score = 1
        scenic_score = 0

        values_above = map[:idxrow,idxcol][::-1] 
        scenic_score += how_many_do_i_see(current_tree_height, values_above)
        tree_scenic_score *= scenic_score
        scenic_score = 0

        values_down = map[idxrow+1:,idxcol]
        scenic_score += how_many_do_i_see(current_tree_height, values_down)
        tree_scenic_score *= scenic_score
        scenic_score = 0

        values_left = map[idxrow,:idxcol][::-1] 
        scenic_score += how_many_do_i_see(current_tree_height, values_left)
        tree_scenic_score *= scenic_score
        scenic_score = 0

        values_right = map[idxrow,idxcol+1:]
        scenic_score += how_many_do_i_see(current_tree_height, values_right)
        tree_scenic_score *= scenic_score
        scenic_score = 0

        if tree_scenic_score > max_scenic_score:
            max_scenic_score = tree_scenic_score

        # print(idxrow, idxcol, max_up)

print(max_scenic_score)

# right answer 392080