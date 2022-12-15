import numpy as np

# ler todas as linhas, como de costume
with open('Challenges\Exc13\input.txt') as f:
    lines = f.read().splitlines()

# converter tudo para uma lista
data = [x for x in lines if len(x) > 0]

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
row_iterator = iter(data)

left_row = next(row_iterator, None)
right_row = next(row_iterator, None)
pair_number = 1
pairs_right_order = []

# JOTA: ver a documentação do < aplicado a listas de python

while(left_row != None and right_row != None):
    if are_right_order(eval(left_row), eval(right_row)):
        pairs_right_order.append(pair_number)
    
    pair_number += 1
    left_row = next(row_iterator, None)
    right_row = next(row_iterator, None)

    print("Right Pairs in loop:", pairs_right_order)

print("Sum: ", sum(pairs_right_order))