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
from termcolor import colored

sys.path.append(os.path.abspath("."))
print(os.path.abspath("."))
from telegram import *

# ler todas as linhas, como de costume
with open('Challenges\Exc25\input.txt') as f:
    lines = f.read().splitlines()

snafu_base10_converter = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    '=': -2
}

base10_snafu_converter = {
    4: '2',
    3: '1',
    2: '0',
    1: '-',
    0: '=',
}

# add in decimal
acc = 0
for snafu_number in lines:
    exp = 0
    sum = 0
    for snafu_digit in snafu_number[::-1]:
        sum += snafu_base10_converter[snafu_digit] * (5 ** exp)
        exp += 1
    acc += sum
    # print(sum)
print(acc)

# convert back to snafu
snafu_number = ''

while acc > 0:
    snafu_number = base10_snafu_converter[(acc+2)% 5] + snafu_number
    acc = (acc+2) // 5

print(snafu_number)

"""
     0        0
     1        1
     2        2
    1=        3 
    1-        4
    10        5
    11        6
    12        7
    2=        8
    2-        9
    20       10
    21       11
"""