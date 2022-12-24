import re
import numpy as np
from operator import itemgetter
import sys
import os
import math
from timeit import default_timer as timer
from tqdm import tqdm
import pickle

with open("Challenges\\Exc18\\cubes.pkl", "rb") as fp:   # Unpickling
    cubes = pickle.load(fp)


print(len(cubes))
print(type(cubes[0]))
print(type(cubes[3100]))