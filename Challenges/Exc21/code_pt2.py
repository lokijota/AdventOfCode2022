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
with open('Challenges\Exc21\input_pt2.txt') as f:
    lines = f.read().splitlines()

numbers = {}
equations = {}

for line in lines:
    parts = line.split(":")
    monkey_equation = parts[0].strip()
    content = parts[1].strip()
    if content[0].isdigit():
        numbers[monkey_equation] = int(content)
    else:
        equations[monkey_equation] = content
    

print("numbers:", len(numbers))
print("equations:", len(equations))

# fazer os replaces e isso e depois avaliar

numbers.pop("humn")
prev_len = -1

while len(equations) > 0:
    for monkey_equation in list(equations):
        equation = equations[monkey_equation]
        for monkey_number in list(numbers):
            if monkey_number in equation:
                equation = equation.replace(monkey_number, str(numbers[monkey_number]))
                equations[monkey_equation] = equation

                try:
                    outcome = eval(equation)
                    numbers[monkey_equation] = outcome
                    del equations[monkey_equation]
                    print("Solved", monkey_equation, "with", equation, "and got", outcome)
                except:
                    pass

    if len(equations) == prev_len:
        print("Did all the replacements I could, remaining equations:", prev_len, ", numbers:", len(numbers))
        break
    else:
        prev_len = len(equations)

print("\nRoot's number after numeric replacements:", equations["root"])

# now do replacements centered on "root"
replacement_done = True
root_expression = equations["root"]
equations.pop("root")

while replacement_done == True:

    for monkey_equation in list(equations):
        equation = equations[monkey_equation]
        if monkey_equation in root_expression:
            root_expression = root_expression.replace(monkey_equation, "(" + str(equations[monkey_equation]) + ")")
            equations.pop(monkey_equation)
            break
    # print("Eq#", len(equations))

    for monkey_number in list(numbers):
        if monkey_number in root_expression:
            root_expression = equation.replace(monkey_number, str(numbers[monkey_number]))
            # numbers.pop(monkey_number)
            # break

    # print(len(numbers))

    if  len(equations) == 0:
        replacement_done = False

root_expression = root_expression.replace(" ", "")
root_expression = root_expression.replace("humn", "x")
root_expression = root_expression.replace("==", "=")
print(root_expression)

# now to go wolfram alpha, input the string, and let it solve it for you ;)