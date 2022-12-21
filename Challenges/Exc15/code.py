import re
import numpy as np
from operator import itemgetter
import sys
import os
import math
from timeit import default_timer as timer

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


def contains(sensor1, sensor2):
  d = math.sqrt(
        (sensor2[0] - sensor1[0])**2 +
        (sensor2[1] - sensor1[1])**2)
  return sensor1[2]  > (d + sensor2[2])

sensors_to_ignore = set()
for sensor1 in sensor_ranges:
    for idx, sensor2 in enumerate(sensor_ranges):
        if sensor1 == sensor2:
            continue
        if contains(sensor1, sensor2):
            print(f"Sensor at {sensor1} fully encloses sensor at {sensor2}")
            sensors_to_ignore.add(idx)

print("Número de sensores a retirar da lista: " + str(len(sensors_to_ignore)))

# remove circles within circles
remove_list = set()

for idx in sorted(sensors_to_ignore, reverse=True):
    del sensor_ranges[idx]
    del locations[idx]

no_beacon_positions = 0

print(f"left edge = {left_edge}, right_edge = {right_edge}")

def something_in_position(row, col):
    if len([1 for location in locations if (location[2] == row and location[3] == col) or (location[0]==row and location[1]==col)]) > 0:
        return True

    return False

def position_in_sensor_range(row, col):
    for location in sensor_ranges:
        if manhathan_dist(row, col, location[0], location[1]) <= location[2]:
            return True
    
    return False

# row = 2000000
# for pos in range(left_edge, right_edge+1):
#     if position_in_sensor_range(row, pos) == True and something_in_position(row, pos) == False:
#         no_beacon_positions += 1

# print("No beacon positions: ", no_beacon_positions)
# SendTelegramMessage("Outcome of part 1 is " + str(len(lines)))

# Part 2

def generate_outer_ring(sensor):
    ring = set()

    lower_limit = 0
    upper_limit = 4000000

    toprow =        sensor[0] - sensor[2] - 1
    bottomrow =     sensor[0] + sensor[2] + 1
    leftcolumn =    sensor[1] - sensor[2] - 1
    rightcolumn =   sensor[1] + sensor[2] + 1

    # top left edge
    row = sensor[0]
    col = leftcolumn
    while row >= toprow and col <= sensor[1]:
        if col > upper_limit or col < lower_limit or row > upper_limit or row<lower_limit:
            col += 1
            row -= 1
            continue
        elif not position_in_sensor_range(row, col):
            ring.add((row, col))

        col += 1
        row -= 1

    # top right edge
    row = toprow
    col = sensor[1]
    while row <= sensor[0] and col <= rightcolumn:
        if col > upper_limit or col < lower_limit or row > upper_limit or row<lower_limit:
            col += 1
            row += 1
            continue
        elif not position_in_sensor_range(row, col):
            ring.add((row, col))

        col += 1
        row += 1

    # bottom left edge
    row = sensor[0]
    col = leftcolumn
    while row <= bottomrow and col <= sensor[1]:
        if col > upper_limit or col < lower_limit or row > upper_limit or row<lower_limit:
            col += 1
            row += 1
            continue
        elif not position_in_sensor_range(row, col):
            ring.add((row, col))

        col += 1
        row += 1

    # bottom right edge
    row = sensor[0]
    col = rightcolumn
    while row <= bottomrow and col >= sensor[1]:
        if col > upper_limit or col < lower_limit or row > upper_limit or row<lower_limit:
            col -= 1
            row += 1
            continue
        elif not position_in_sensor_range(row, col):
            ring.add((row, col))

        col -= 1
        row += 1

    return ring


print("start")
ring = set()
# print(position_in_sensor_range(11, 14))
SendTelegramMessage("Start part 2")
start = timer()
for idx, sensor in enumerate(sensor_ranges):
    ring = ring.union(generate_outer_ring(sensor))
    if len(ring) == 1:
        break # note: this is not really accurate, but it's good enough for this problem
    print(f"Ring# tested {idx}, ring size = {len(ring)}")
    SendTelegramMessage(f"Ring# tested {idx}, ring size = {len(ring)}")
end = timer()
print("Elapsed time:", end - start)
print("end")

if len(ring) > 0:
    print(list(ring))
    SendTelegramMessage("Outcome of part 2 is " + str(ring))
    SendTelegramMessage("Outcome of part 2 has tunning frequency " + str(list(ring)[0][0] + list(ring)[0][1]*4000000))
else:
    print("Nothing found")
    SendTelegramMessage("zilch")


# tuning_frequncy = 0
# # for row in range(0, 4000000+1):
#     for col in range(0, 4000000+1):
#         if position_in_sensor_range(row, col) == False:
#             tuning_frequncy = row + col*4000000
#             print("Tunning frequency: ", str(tuning_frequncy))
#             SendTelegramMessage("Outcome of part 2 is " + str(tuning_frequncy))
#             break
#     print("Row: ", row, end=", ")


