import re
import numpy as np
from operator import itemgetter
import sys
import os
import math
from timeit import default_timer as timer
from tqdm import tqdm

sys.path.append(os.path.abspath("."))
print(os.path.abspath("."))
from telegram import *

# ler todas as linhas, como de costume
with open('Challenges\Exc18\input.txt') as f:
    lines = f.read().splitlines()

cubes = [np.array([int(parts) for parts in line.split(",")]) for line in lines]

touching = 0
for cube1 in tqdm(cubes):
    for cube2 in cubes:
        dist = np.linalg.norm(cube2-cube1)
        if dist == 1:
            touching += 1
    
print(touching)
print(len(cubes)*6)
print(len(cubes)*6-touching)