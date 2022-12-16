import numpy as np
np.set_printoptions(threshold=np.inf) #or False to revert to default

# ler todas as linhas, como de costume
with open('Challenges\Exc14\input.txt') as f:
    lines = f.read().splitlines()

# split in xy pairs, then trim, then split the xy pairs in x and y, and then convert to int 
rock_paths = []
rock_paths.append([[list(map(int, y.strip().split(","))) for y in x.split("->")] for x in lines])
rock_paths = rock_paths[0]
# print(rock_paths)

max_x = 0
min_x = 1000
max_y = 0
min_y = 0

for rock_path in rock_paths:
    for coordinate in rock_path:
        if coordinate[0] > max_x:
            max_x = coordinate[0]
        elif coordinate[0] < min_x:
            min_x = coordinate[0]
        
        if coordinate[1] > max_y:
            max_y = coordinate[1]
        # min is zero, as it's the top of the map
        # elif coordinate[1] < min_y:
        #      min_y = coordinate[1]

base_col = min_x
base_row = min_y

print(min_x, max_x, min_y, max_y)

# create a matrix with the size of the map
cave = np.zeros((max_y - min_y + 1, max_x - min_x + 1), dtype=int)
print(cave.shape)

# fill the matrix with the rock paths
for rock_path in rock_paths:
    for pos in range(len(rock_path) - 1):
        x1 = rock_path[pos][0] - base_col
        y1 = rock_path[pos][1] - base_row
        x2 = rock_path[pos+1][0] - base_col
        y2 = rock_path[pos+1][1] - base_row

        # check if the rock path is horizontal
        if y1 == y2:
            # print("horizontal")
            # check if the rock path is to the right
            if x1 < x2:
                # print("to the right")
                cave[y1, x1:x2+1] = 1 
            # check if the rock path is to the left
            elif x1 > x2:
                # print("to the left")
                cave[y1, x2:x1+1] = 1

        # check if the rock path is vertical
        elif x1 == x2:
            # print("vertical")
            # check if the rock path goes downwards
            if y1 < y2:
                # print("to the bottom")
                cave[y1:y2+1, x1] = 1
            # check if the rock path goes upwards
            elif y1 > y2:
                cave[y2:y1+1, x1] = 1
        # else:
        #     print("error: rock path not horizontal or vertical")

# print(cave)

def is_free(row, col):
    # check bounds
    if row < 0 or row >= cave.shape[0] or col < 0 or col >= cave.shape[1]:
        # return False
        raise Exception("Out of bounds of cave", row, col, cave.shape)

    # now check if position is free
    if cave[row, col] == 1 or cave[row, col] == 2:
        return False
    else:
        return True

def drop_sand(row, col):

    # np.savetxt('Challenges\Exc14\cave_end_ok.txt', cave, fmt ='%.0f')

    row -= base_row
    col -= base_col

    if sand_units > 0 and row+base_row == 0 and col+base_col == 500 and is_free(row,col) and not is_free(row+1,col) and not is_free(row+1,col-1) and not is_free(row+1,col+1):
        # enchemos até acima
        return False

    # fall down one position if possible
    if is_free(row+1, col):
        cave[row+1,col] = 2
        cave[row, col] = 0
        return drop_sand(row+1+base_row, col+base_col)
    
    # it isn't possible, so let's try down and left, but first check if we didn't hit the left wall or bottom wall
    elif row+1 == cave.shape[0] or col-1 < 0: 
        return False
    # if within limits, move
    elif row+1 < cave.shape[0] and col-1 >= 0  and is_free(row+1, col-1):
        cave[row+1, col-1] = 2
        cave[row, col] = 0 # JOTA: DESDE QUE N SEJA FORA DO ARRAY....
        return drop_sand(row+1+base_row, col-1+base_col)
    
    # and here we try doing down and right / test for bottom wall and right wall
    elif row+1 == cave.shape[0] or col+1 == cave.shape[1]:
        return False
    elif row+1 < cave.shape[0] and col+1 < cave.shape[1] and is_free(row+1, col+1):
        cave[row+1, col+1] = 2
        cave[row, col] = 0
        return drop_sand(row+1+base_row, col+1+base_col)
    else:
        return True


# start dropping stand from the top - x=500, y=0
sand_units = 0

# print(cave)
# np.savetxt('Challenges\Exc14\cave_start.txt', cave)

try:
    while drop_sand(0, 500):
        sand_units += 1
    # np.savetxt('Challenges\Exc14\cave_end_ok.txt', cave, fmt ='%.0f')
except Exception as e: 
    print(e)
    # np.savetxt('Challenges\Exc14\cave_end_offmap.txt', cave, fmt ='%.0f')

print("Total sand units: ", sand_units+1) # +1 to account for the top of the pyramid one

#finally!!! 23416 answer -- note that I added last row to both data files... that was evil.