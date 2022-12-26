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

sys.path.append(os.path.abspath("."))
print(os.path.abspath("."))
from telegram import *

# ler todas as linhas, como de costume
with open('Challenges\Exc19\input_debug.txt') as f:
    lines = f.read().splitlines()

regex = "^Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.$"
blueprint_matches = [re.findall(regex, line) for line in lines]
# [[('1', '4', '4', '4', '17', '4', '20')], [('2', '3', '3', '2', '12', '2', '10')], 

blueprints = {}
for blueprint_match in blueprint_matches:
    bpm = blueprint_match[0]

    blueprint = {}
    blueprint['orebot'] = np.array([int(bpm[1]), 0,0])
    blueprint['claybot'] = np.array([int(bpm[2]), 0,0])
    blueprint['obsidianbot'] = np.array([int(bpm[3]), int(bpm[4]),0])
    blueprint['geodebot'] = np.array([int(bpm[5]), 0, int(bpm[6])])

    blueprints["bp" + bpm[0]] = blueprint

# print(blueprints)

"""
Class to represent the state of the game at a given time
"""
class GameState(object):
    def __init__(self, ores=0, clays=0, obsidians=0, geodes=0, orebots=1, claybots=0, obsidianbots=0, geodebots=0, constructingbot="", ticks=0):
        self.ores = ores
        self.clays = clays
        self.obsidians = obsidians
        self.geodes = geodes
        self.orebots = orebots
        self.claybots = claybots
        self.obsidianbots = obsidianbots
        self.geodebots = geodebots
        self.constructing = constructingbot # Orebot (OB), Claybot (CB), Obsidianbot (OB), Geodebot (GB) or "" (nothing)
        self.ticks = ticks 

    def extract_minerals(self):
        self.ores += self.orebots
        self.clays += self.claybots
        self.obsidians += self.obsidianbots
        self.geodes += self.geodebots

    def possible_construction(self, blueprint):
        choices = []

        if self.ores >= blueprint['orebot'][0]:
            choices += ["OB"]
        if self.ores >= blueprint['claybot'][0]:
            choices += ["CB"]
        if self.ores >= blueprint['obsidianbot'][0] and self.clays >= blueprint['obsidianbot'][1]:
            choices += ["OB"]
        if self.ores >= blueprint['geodebot'][0] and self.obsidians >= blueprint['geodebot'][2]:
            choices += ["GB"]

        choices += [""] # don't construct anything

        return choices

    def construct_bot(self, blueprint):
        # order is relevant just to see # of geodes grow faster
        # geobots are constructed first, then obsidianbots, then claybots, then orebots
        if self.constructing == "GB":
            self.geodebots += 1
            self.ores -= blueprint['geodebot'][0]
            self.obsidians -= blueprint['geodebot'][2]
        elif self.constructing == "OB":
            self.obsidianbots += 1
            self.ores -= blueprint['obsidianbot'][0]
            self.clays -= blueprint['obsidianbot'][1]
        elif self.constructing == "CB":
            self.claybots += 1
            self.ores -= blueprint['claybot'][0]
        elif self.constructing == "OB":
            self.orebots += 1
            self.ores -= blueprint['orebot'][0]
        
        self.constructing = ""

quality_level = 0
for bpnumber in range(1, 31):
    bp_name = "bp" + str(bpnumber)

    initial_state = GameState()
    game_queue = deque([initial_state])
    geode_max = 0
    max_ticks = 0

    start = timer()
    while len(game_queue) > 0:
        state = game_queue.popleft() # game_queue.pop(0)
        if state.ticks > 24: # time's up, just remove from queue
            continue
        # elif state.ticks > max_ticks:
        #     max_ticks = state.ticks
        #     SendTelegramMessage("New max ticks: " + str(max_ticks) + ",  len q =" + str(len(game_queue)))

        for construction in state.possible_construction(blueprints[bp_name]):
            new_state = GameState(state.ores, state.clays, state.obsidians, state.geodes, state.orebots, state.claybots, state.obsidianbots, state.geodebots, construction, state.ticks + 1)
            new_state.extract_minerals()
            new_state.construct_bot(blueprints[bp_name])
            game_queue.append(new_state)

            if state.geodes > geode_max:
                geode_max = state.geodes
                print("New max geodes: " + str(geode_max) + " at tick " + str(state.ticks) + ", q size:" + str(len(game_queue)) + ", geodebots:" + str(new_state.geodebots))
                # SendTelegramMessage("New max geodes: " + str(geode_max) + " at tick " + str(state.ticks))

    quality_level += bpnumber*geode_max
    SendTelegramMessage("Quality level with blueprint " + str(bpnumber) + " completed is " + str(quality_level))

end = timer()
print("Final quality level: ", quality_level)
print("Elapsed time: " + str(end - start))
SendTelegramMessage("Elapsed time: " + str(end - start))
