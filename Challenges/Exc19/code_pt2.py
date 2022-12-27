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
with open('Challenges\Exc19\input_pt2.txt') as f:
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
    def __init__(self, ores=0, clays=0, obsidians=0, geodes=0, orebots=1, claybots=0, obsidianbots=0, geodebots=0, constructingbot="", ticks=0, construction_history = []):
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
        self.construction_history = [] # to speed up construction_history.copy()

    def extract_minerals(self):
        self.ores += self.orebots
        self.clays += self.claybots
        self.obsidians += self.obsidianbots
        self.geodes += self.geodebots

    def possible_construction(self, blueprint):
        # order is relevant just to see # of geodes grow faster
        # geobots are constructed first, then obsidianbots, then claybots, then orebots
        choices = []

        # do_ore_bot = False
        # do_clay_bot = False

        choices += [""] # don't construct anything

        if self.ores >= blueprint['orebot'][0]:
            choices += ["ORB"]
            # do_ore_bot = (self.orebots == 0)

        if self.ores >= blueprint['claybot'][0]:
            choices += ["CLB"]
            # do_clay_bot = (self.claybots == 0)

        # if we can do an ore bot or a clay bot and there's none of them yet, don't generate the "skip" option
        # if (do_ore_bot == False) or (do_clay_bot == False):
            # choices += [""]

        if self.ores >= blueprint['obsidianbot'][0] and self.clays >= blueprint['obsidianbot'][1]:
            choices += ["OBB"]

        if self.ores >= blueprint['geodebot'][0] and self.obsidians >= blueprint['geodebot'][2]:
            choices += ["GEB"]
        
        return choices

    def construct_bot(self, blueprint):

        self.construction_history += [self.constructing]

        if self.constructing == "ORB":
            self.orebots += 1
            self.ores -= blueprint['orebot'][0]
        elif self.constructing == "CLB":
            self.claybots += 1
            self.ores -= blueprint['claybot'][0]
        elif self.constructing == "OBB":
            self.obsidianbots += 1
            self.ores -= blueprint['obsidianbot'][0]
            self.clays -= blueprint['obsidianbot'][1]
        elif self.constructing == "GEB":
            self.geodebots += 1
            self.ores -= blueprint['geodebot'][0]
            self.obsidians -= blueprint['geodebot'][2]
        
        self.constructing = ""

    def state_score(self):
        # return self.orebots + self.claybots*1.5 + self.obsidianbots*10 + self.geodebots*100
        return self.orebots + self.claybots*1.5 + self.obsidianbots*50 + self.geodebots*200


multiplication_total = 1
for bpnumber in range(1, 4):
    print("**** Starting Blueprint", bpnumber, "****")
    bp_name = "bp" + str(bpnumber)

    initial_state = GameState()
    game_queue = deque([initial_state])
    geode_max = 0
    max_ticks = 0

    max_scores_per_tick = np.zeros(32+3)

    fastest_geobot = 32+1

    states_checked = 0
    states_bypassed = 0

    start = timer()
    while len(game_queue) > 0:
        state = game_queue.pop() # game_queue.popleft()
        states_checked += 1 # isto devia estar depois das heurísticas -- ou entar contar os dois estados

        # let's try this: if we're past x ticks and we haven't constructed a geobot yet, let's not bother
        if state.ticks > fastest_geobot +1 and state.geodebots == 0:
            states_bypassed += 1
            continue

        for construction in state.possible_construction(blueprints[bp_name]):
            new_state = GameState(state.ores, state.clays, state.obsidians, state.geodes, state.orebots, state.claybots, state.obsidianbots, state.geodebots, construction, state.ticks + 1, state.construction_history)
            new_state.extract_minerals()

            if new_state.constructing == "GEB" and fastest_geobot > new_state.ticks:
                fastest_geobot = new_state.ticks
                print("++ Fastest 1st geobot - At ticks", fastest_geobot)
                # print(" ... has construction history:", new_state.construction_history)

            new_state.construct_bot(blueprints[bp_name]) # this clears the contructing variable, so keeping it after the previous if

            if new_state.geodes > geode_max:
                geode_max = new_state.geodes
                print("New max geodes: " + str(geode_max) + " at tick " + str(state.ticks) + ", q size:" + str(len(game_queue)) + ", geodebots:" + str(new_state.geodebots))
                # print(" ... has construction history:", new_state.construction_history)

            state_score = new_state.state_score()
            if state_score > max_scores_per_tick[new_state.ticks]:
                max_scores_per_tick[new_state.ticks] = state_score
            elif state_score < max_scores_per_tick[new_state.ticks-3]:
                states_bypassed += 1
                continue

            if new_state.ticks < 32: # no need to add to queue if we're already past 24 ticks
                game_queue.append(new_state)

    end = timer()
    print("Elapsed time for blueprint: " + str(bpnumber) + " was " + str(end - start))
    print("Geode max for blueprint: " + str(geode_max))
    
    multiplication_total *= geode_max
    print(">>>> Mult total with blueprint " + str(bpnumber) + " completed is " + str(multiplication_total) + ", checked # states: " + str(states_checked) + ", of which #bypassed=" + str(states_bypassed))
    SendTelegramMessage("Mult total with blueprint " + str(bpnumber) + " completed is " + str(multiplication_total))

print("Final Multiplication total: ", multiplication_total)