import numpy as np
from numpy.linalg import norm

# read all the lines
with open('Challenges\Exc9\input.txt') as f:
    lines = f.read().splitlines()

# start by building a a list with all the movements of the Heads, just because I like using up memory instead of keeping it efficient and step by step
# doing it like this is really absurd. also note I have to use copy() or the list would just have duplicated results
current_pos = np.array([0,0]) #x,y
heads_path = []

heads_path.append(current_pos.copy())

tail_positions = { (current_pos[0], current_pos[1]) }

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

print(heads_path)


def next_tails_position(current_head_pos, current_tail_pos):
    dif = current_head_pos-current_tail_pos

    print(current_head_pos, current_tail_pos, dif)
    if norm(current_head_pos - current_tail_pos) < 2:
        # print("not moving tails", norm(dif))
        a = 1
    else:
        print(" - should move tails, distance: ", norm(dif))

        # simpler cases - up down left right movement
        if dif[0] != 0 and dif[1] == 0: # horizontal movement
            current_tail_pos[0] += dif[0]/2  
            print(" - moved tails to ", current_tail_pos)
        elif dif[0] == 0 and dif[1] != 0: # vertical movement
            current_tail_pos[1] += dif[1]/2
            print(" - moved tails to ", current_tail_pos)
        else: #diagonal movement
            # if current_head_pos[0] == 4 and current_head_pos[1] == 3:
            #     a=2

            if dif[0] > 0:
                current_tail_pos[0] += 1
            else:
                current_tail_pos[0] -= 1

            if dif[1] > 0:
                current_tail_pos[1] += 1
            else:
                current_tail_pos[1] -= 1

            # # if dif[0] > 0:
            # current_tail_pos[0] += -(dif[0]//-2)  
            # # else:
            #     # current_tail_pos[0] += dif[0]//2  

            # if dif[1] > 0:
            #     current_tail_pos[1] += -(dif[1]//-2)
            # else:
            #     current_tail_pos[1] += dif[1]//-2

            print(" - moved tails to ", current_tail_pos)
            # -(a // -b) hint from https://stackoverflow.com/questions/14822184/is-there-a-ceiling-equivalent-of-operator-in-python

        tail_positions.add((current_tail_pos[0],current_tail_pos[1]))

        # print("Tail positions set:", tail_positions)


current_tail_pos = np.array([0,0]) #x,y

# main loop
for head_pos in heads_path:
    next_tails_position(head_pos, current_tail_pos)

print("Set size: ", len(tail_positions))

# 6236