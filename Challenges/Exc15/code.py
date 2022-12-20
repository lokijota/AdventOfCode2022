import re
import numpy as np
from operator import itemgetter
import sys
import os

sys.path.append(os.path.abspath("."))
print(os.path.abspath("."))
from telegram import *

# funções necessárias

def manhathan_dist(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

# ler e processar o ficheiro de dados do exercício

with open('Challenges\Exc15\input.txt') as f:
    lines = f.read().splitlines()

regex = "^Sensor at x=([+-]?\d+), y=([+-]?\d+): closest beacon is at x=([+-]?\d+), y=([+-]?\d+)$"
locations = [re.findall(regex, line) for line in lines]
locations = [[int(location[0][1]), int(location[0][0]), int(location[0][3]), int(location[0][2])] for location in locations]
# print(locations)
# note: change from x,y to row,col => inverting order of coordinates
sensor_ranges = [[location[0], location[1], manhathan_dist(location[0], location[1], location[2], location[3])] for location in locations]
# print(sensor_ranges)    

left_edge = min([location[1] - location[2] for location in sensor_ranges])
right_edge = max([location[1] + location[2] for location in sensor_ranges])
no_beacon_positions = 0

print(left_edge, right_edge)


def something_in_position(row, col):
    if len([1 for location in locations if (location[2] == row and location[3] == col) or (location[0]==row and location[1]==col)]) > 0:
        return True

    return False

def position_in_sensor_range(row, col):
    for location in sensor_ranges:
        if manhathan_dist(row, col, location[0], location[1]) <= location[2]:
            return True
    
    return False

row = 2000000
for pos in range(left_edge, right_edge+1):
    if position_in_sensor_range(row, pos) == True and something_in_position(row, pos) == False:
        no_beacon_positions += 1

print(no_beacon_positions)

SendTelegramMessage("Outcome of part 1 is " + str(len(lines)))