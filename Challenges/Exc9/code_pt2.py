import numpy as np
from numpy.linalg import norm

# read all the lines
with open('Challenges\Exc9\input.txt') as f:
    lines = f.read().splitlines()

# start by building a a list with all the movements of the Heads, just because I like using up memory instead of keeping it efficient and step by step
# doing it like this is really absurd. also note I have to use copy() or the list would just have duplicated results. this however allowed me to 
# have a relatively smooth ride on the part 2 of challenge 9

current_pos = np.array([0,0]) #x,y
heads_path = []
heads_path.append(current_pos.copy())

for command in lines:
    parts = command.split(" ")

    for _ in range(int(parts[1])):

        if parts[0] == "D":
            current_pos[1] -= 1
        elif parts[0] == "U":
            current_pos[1] += 1
        elif parts[0] == "L":
            current_pos[0] -= 1
        elif parts[0] == "R":
            current_pos[0] += 1

        heads_path.append(current_pos.copy())

print(len(heads_path))

def calculate_next_position(current_head_pos, current_tail_pos):
    next_pos = current_tail_pos.copy()
    dif = current_head_pos-next_pos

    if norm(current_head_pos - next_pos) >= 2:

        if dif[0] != 0 and dif[1] == 0: # horizontal movement
            next_pos[0] += dif[0]/2  
        elif dif[0] == 0 and dif[1] != 0: # vertical movement
            next_pos[1] += dif[1]/2
        else: #diagonal movement

            if dif[0] > 0:
                next_pos[0] += 1
            else:
                next_pos[0] -= 1

            if dif[1] > 0:
                next_pos[1] += 1
            else:
                next_pos[1] -= 1

    return next_pos

# main loop
follower_path = []


# basically run the generation process 9 times, and the last path is the tail's one
for _ in range(9):
    current_follower_pos = np.array([0,0]) #x,y

    for head_pos in heads_path:
        pos = calculate_next_position(head_pos, current_follower_pos)
        follower_path.append(pos)
        current_follower_pos = pos

    heads_path = follower_path
    follower_path = []

# calculate distinct movements of the last piece, the tail
tail_positions = set()

for pos in heads_path:
    tail_positions.add((pos[0],pos[1]))

print("Set size: ", len(tail_positions))

# 6236