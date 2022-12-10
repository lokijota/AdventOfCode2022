# read all the lines
with open('Challenges\Exc6\input.txt') as f:
    lines = f.readlines()


for idx, char in enumerate(lines[0]):
    a_set = set(lines[0][idx:idx+14])

    if len(a_set) == 14:
        print(a_set)
        print(idx+14) #1909 and 3380 for part 1 and 2 respectively
        break