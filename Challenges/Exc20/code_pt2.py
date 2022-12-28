import re
import numpy as np
from operator import itemgetter
import sys
import os
import math
from timeit import default_timer as timer
from tqdm import tqdm
import pickle
from collections import deque
import copy


sys.path.append(os.path.abspath("."))
print(os.path.abspath("."))
from telegram import *

# ler todas as linhas, como de costume
with open('Challenges\Exc20\input.txt') as f:
    lines = f.read().splitlines()

cyphertext = [[idx, int(num)*811589153] for idx, num in enumerate(lines)]
worklist = deque(copy.deepcopy(cyphertext))
listsize = len(worklist)

for i in range(10):
    for cyphernum in cyphertext:
        # procurar o elemento na worklist e ver a posição
        idx = worklist.index(cyphernum)
        element = worklist[idx]

        # remover o elemento da worklist
        del worklist[idx]

        newpos = (idx+element[1]) % (listsize-1) # that -1 is the secret sauce here

        # inserir o elemento na worklist 
        worklist.insert(newpos, element)
        # print([worklist[i][1] for i in range(listsize)])

# print([worklist[i][1] for i in range(listsize)])

# now find the element zero
for idx, element in enumerate(worklist):
    if element[1] == 0:
        print("Found zero at idx:", idx, element)
        break

# print(worklist)

val1000 = worklist[(idx+1000) % listsize][1]
val2000 = worklist[(idx+2000) % listsize][1]
val3000 = worklist[(idx+3000) % listsize][1]
print("Final number is", val1000 + val2000 + val3000)
print("Parts:", val1000, val2000, val3000)

# 3390007892081