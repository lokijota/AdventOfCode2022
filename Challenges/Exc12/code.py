import numpy as np

# read all the lines
with open('Challenges\Exc12\input.txt') as f:
    lines = f.read().splitlines()

# read everything to an array and identify starting and end positions
heightmap = np.empty((100,142), dtype = int)
startpos = [0,0]
endpos = [0,0]

Schar = ord("S")
Echar = ord("E")

heights = []

for line in lines:
    # convert to int values 
    heights.append([ord(x) - ord("a") + 1 for x in row])
    print(heights)

# from the heightmap, build the graph
# if some connection has distance > 1, skip
# at the same time, set the start and end positions


# apply djiskra
