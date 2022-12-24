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
with open('Challenges\Exc21\input.txt') as f:
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

print("Root's number:", numbers["root"])