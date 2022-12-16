import numpy as np
import functools

# ler todas as linhas, como de costume
with open('Challenges\Exc13\input_debug.txt') as f:
    lines = f.read().splitlines()

# converter tudo para uma lista
data = [eval(x) for x in lines if len(x) > 0]
data.append([[2]])
data.append([[6]])

print("Total rows: ", len(data))

# função para comparar
def are_right_order(left, right):

    # if both are ints
    if type(left) == int and type(right) == int:
        if left < right: 
            return True
        elif left > right:
            return False
        else:
            return None # signal to continue

    # else continue testing
    # but there's still a chance both are ints! <----

    # if one is a list and the other an int, convert the 2nd to list and call again
    if type(left) == int and type(right) == list:
        return are_right_order([left], right)
    elif type(left) == list and type(right) == int:
        return are_right_order(left, [right])

    # if we get here, both should be lists
    if len(left) > 0 and len(right) > 0:
        result = are_right_order(left[0], right[0])
        if result != None:
            return result
        
        return are_right_order(left[1:], right[1:])
    elif len(left) < len(right):
        return True   
    elif len(left) > len(right):
        return False
    else:
        return None
    
# iterar sobre cada par de linhas
next_round_end_pos = len(data)-1
current_round_pos = 0

for start in range(len(data)-1):

    exchanges = 0

    for current_round_pos in range(next_round_end_pos):

        if are_right_order(data[current_round_pos], data[current_round_pos+1]) == False:
            data[current_round_pos], data[current_round_pos+1] = data[current_round_pos+1], data[current_round_pos]
            exchanges += 1

        # print(".", end="")

    print("*Exchanges", exchanges, " for start", start)

    next_round_end_pos -= 1

# find the positions~
sorted_str_list = [str(x) for x in data]

# print(sorted_list)

pos_start = -1
pos_end = -1
for idx, item in enumerate(sorted_str_list):
    if item == "[[6]]":
        pos_end = idx
    elif item == "[[2]]":
        pos_start = idx


print(pos_start, pos_end, (pos_start+1) * (pos_end+1))

with open('Challenges\Exc13\output.txt', 'w') as fp:
    for item in data:
        fp.write("%s\n" % item)
    print('Done')

# 35334 is too high