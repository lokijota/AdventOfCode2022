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
with open('Challenges\Exc24\input.txt') as f:
    lines = f.read().splitlines()

################### implementação de grafo de: https://www.udacity.com/blog/2021/10/implementing-dijkstras-algorithm-in-python.html
 
class Graph(object):
    def __init__(self, nodes, init_graph):
        self.nodes = nodes
        self.graph = self.construct_graph(nodes, init_graph)
        
    def construct_graph(self, nodes, init_graph):
        '''
        This method makes sure that the graph is symmetrical. In other words, if there's a path from node A to B with a value V, there needs to be a path from node B to node A with a value V.
        '''

        # jota -- preemptive 
        print("original node nb", len(nodes))
        while True:
            dead_nodes = []
            for node_name in init_graph.keys():
                if len(init_graph[node_name]) == 0 and node_name != "end_node":
                    dead_nodes.append(node_name)

            for dead_node_name in dead_nodes:
                init_graph.pop(dead_node_name, None)
                nodes.remove(dead_node_name)

            # nothing more to delete
            if len(dead_nodes) == 0:
                break

            # also remove the edges that point to dead nodes
            for node in init_graph.keys():
                edges_dict = init_graph[node].keys()
                for dead_node in dead_nodes:
                    if dead_node in edges_dict:
                        init_graph[node].pop(dead_node, None)            
        print("prunned:", len(nodes))



        graph = {}
        for node in nodes:
            graph[node] = {}
        
        graph.update(init_graph)

        # for node, edges in graph.items():
        #     for adjacent_node, value in edges.items():
        #         if graph[adjacent_node].get(node, False) == False:
        #             graph[adjacent_node][node] = value
                    
        return graph
    
    def get_nodes(self):
        "Returns the nodes of the graph."
        return self.nodes
    
    def get_outgoing_edges(self, node):
        "Returns the neighbors of a node."
        connections = []
        for out_node in self.nodes:
            if self.graph[node].get(out_node, False) != False:
                connections.append(out_node)
        return connections
    
    def value(self, node1, node2):
        "Returns the value of an edge between two nodes."
        return self.graph[node1][node2]

def dijkstra_algorithm(graph, start_node):

    unvisited_nodes = list(graph.get_nodes())
 
    # We'll use this dict to save the cost of visiting each node and update it as we move along the graph   
    shortest_path = {}
 
    # We'll use this dict to save the shortest known path to a node found so far
    previous_nodes = {}
 
    # We'll use max_value to initialize the "infinity" value of the unvisited nodes   
    max_value = sys.maxsize
    for node in unvisited_nodes:
        shortest_path[node] = max_value
    # However, we initialize the starting node's value with 0   
    shortest_path[start_node] = 0
    
    # The algorithm executes until we visit all nodes
    jotastart = timer()
    while unvisited_nodes:

        # The code block below finds the node with the lowest score
        current_min_node = None
        for node in unvisited_nodes: # Iterate over the nodes
            if current_min_node == None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node
                
        # The code block below retrieves the current node's neighbors and updates their distances
        neighbors = graph.get_outgoing_edges(current_min_node)
        for neighbor in neighbors:
            tentative_value = shortest_path[current_min_node] + graph.value(current_min_node, neighbor)
            if tentative_value < shortest_path[neighbor]:
                shortest_path[neighbor] = tentative_value
                # We also update the best path to the current node
                previous_nodes[neighbor] = current_min_node
 
        # After visiting its neighbors, we mark the node as "visited"
        unvisited_nodes.remove(current_min_node)

        # jota debug
        if len(unvisited_nodes) % 500 == 0:
            jotaend = timer()
            print("Unvisited nodes left: ", len(unvisited_nodes), ", elapsed secs=", jotaend-jotastart)
            jotastart = timer()
    
    return previous_nodes, shortest_path

def print_result(previous_nodes, shortest_path, start_node, target_node):
    path = []
    node = target_node
    
    while node != start_node:
        path.append(node)
        node = previous_nodes[node]
 
    # Add the start node manually
    path.append(start_node)
    
    print("We found the following best path with a value of {}.".format(shortest_path[target_node]))
    print(" -> ".join(reversed(path)))
    print("#step = ", len(path)-1)

####################### fim da implementação de grafo

# set useful variables. note I'm excluding the outer walls from the coordinate system to simplify math operations
height = len(lines)-2 
width = len(lines[0])-2
start_pos = (-1, 0)
end_pos = (height, width-1)

# extract the blizzard positions, and make them 0-based
blizzards_at_start = [(row-1,col-1, the_char) for row, line in enumerate(lines) for col, the_char in enumerate(line) if the_char in ['<', '>', '^', 'v']]

def blizzards_at_minute(start_blizzards, minute, width, height):
    blizzards_up = [((row-minute)%height, col, the_char) for row, col, the_char in start_blizzards if the_char == '^']
    blizzards_down = [((row+minute)%height, col, the_char) for row, col, the_char in start_blizzards if the_char == 'v']
    blizzards_left = [(row, (col-minute)%width, the_char) for row, col, the_char in start_blizzards if the_char == '<']
    blizzards_right = [(row, (col+minute)%width, the_char) for row, col, the_char in start_blizzards if the_char == '>']

    return blizzards_up + blizzards_down + blizzards_left + blizzards_right

def free_positions_at_minute(start_blizzards, minute, width, height):
    blizzards = blizzards_at_minute(start_blizzards, minute, width, height)
    blizzard_coords = list(map(lambda x: (x[0], x[1]), blizzards)) # isolating this as it makes for a much faster list compreenhension execution time
    return [(row, col) for row in range(height) for col in range(width) if (row, col) not in blizzard_coords]

possible_relative_moves = [(-1,0), (1,0), (0,0), (0,-1), (0,1)] # staying in place is also an option

def get_possible_moves(start_blizzards, t0, width, height, previous_connections = []):
    connections = []

    t0_free_positions = free_positions_at_minute(start_blizzards, t0, width, height)

    possible_moves_from_t0 = []
    for t0_free_position in t0_free_positions:
        possible_moves_from_t0 += [ (t0_free_position[0], t0_free_position[1], t0_free_position[0] + prm[0], t0_free_position[1] + prm[1]) for prm in possible_relative_moves if (t0_free_position[0] + prm[0] < height) and (t0_free_position[0] + prm[0] >= 0) and (t0_free_position[1] + prm[1] < width) and (t0_free_position[1] + prm[1] >= 0) ]

    # optimization -- filter out all the positions that are at a manhattan distance > t from the starting position
    # (or >=, I'm not sure yet). Or another alternative is to filter based on a list of coordinates that are  in prev
    # connections. for example, on the very first step you can only move from -1,0 to 0,0, so t0_free_positions can be 
    # filtered based on that fact.

    t1_free_positions = free_positions_at_minute(start_blizzards, t0+1, width, height)

    # agora quero ver a intersecção entre o possible_moves_from_t0 e t1_free_positions, olhando para a posição final de possible moves from t0
    connections = [pmt0 for pmt0  in possible_moves_from_t0 if (pmt0[2], pmt0[3]) in t1_free_positions]

    return connections



def print_map(blizzards, width, height):
    map = np.full((height,width), ".")

    for blizzard in blizzards:
        map[blizzard[0], blizzard[1]] = blizzard[2]

    for row in map:
        for col in row:
            if col in ['<', '>', '^', 'v']:
                print(colored(col, 'red'), end='')
            else:
                print(col, end='')
        print()
    print()

# print_map(blizzards_at_start, width, height)
# print(free_positions_at_minute(blizzards_at_start, 1, width, height))

# create the node
init_graph = {}
init_graph["start_node"] = {}
# init_graph["start_node"]["t0_0_0"] = 1 # this would only work if the position  0,0 was free at t=0
init_graph["end_node"] = {}

start_node_connected = False
for t in range(380):
    start = timer()
    moves = get_possible_moves(blizzards_at_start, t, width, height)

    # print_map(blizzards_at_minute(blizzards_at_start, t, width, height), width, height)

    if start_node_connected == False:
        for move in moves:
            if move[0] == 0 and move[1] == 0:
                init_graph["start_node"]["t" + str(t) + "_0_0"] = 1
                start_node_connected = True
                break

    # if no nodes are connected to the starting point, just skip this round
    if start_node_connected == False:
        continue

    for move in moves:
        origin_node = "t" + str(t) + "_" + str(move[0]) + "_" + str(move[1])
        target_node = "t" + str(t+1) + "_" + str(move[2]) + "_" + str(move[3])

        # node names can be repeated due to different ways to get to them (if I'm not mistaken)
        if origin_node not in init_graph:
            init_graph[origin_node] = {}
        if target_node not in init_graph:
            init_graph[target_node] = {}
        init_graph[origin_node][target_node] = 1

        # add a connection to the end node if it exists
        if move[2] == end_pos[0]-1 and move[3] == end_pos[1]:
            # print(target_node + " is connected to the end node (from target_node)")
            init_graph[target_node]["end_node"] = 1
    
    end = timer()
    print("Time to process round " + str(t) + ": " + str(end - start) + " seconds, nodes in graph = ", len(init_graph))


graph = Graph(list(init_graph.keys()), init_graph)

print("Starting dijkstra algorithm...")
start = timer()
previous_nodes, shortest_path = dijkstra_algorithm(graph=graph, start_node="start_node")
end = timer()
print("Time to process dijkstra: " + str(end - start) + " seconds")


if "end_node" not in previous_nodes:
    print("No path found")
else:
    print_result(previous_nodes, shortest_path, "start_node", "end_node")

"""
...
t19_4_4 is connected to the end node
t20_4_4 is connected to the end node
t20_4_4 is connected to the end node
t20_4_4 is connected to the end node
t21_4_4 is connected to the end node
t21_4_4 is connected to the end node
t21_4_4 is connected to the end node
t22_4_4 is connected to the end node
t22_4_4 is connected to the end node
"""


"""
Time to process dijkstra: 35378.4729955 seconds
We found the following best path with a value of 373.
start_node -> t1_0_0 -> t2_0_0 -> t3_1_0 -> t4_1_0 -> t5_1_1 -> t6_2_1 -> t7_2_2 -> t8_3_2 -> t9_4_2 -> t10_4_1 -> t11_4_1 -> t12_3_1 -> t13_3_2 -> t14_2_2 -> t15_1_2 -> t16_1_2 -> t17_1_3 -> t18_1_2 -> t19_0_2 -> t20_0_2 -> t21_0_3 -> t22_0_4 -> t23_1_4 -> t24_0_4 -> t25_0_5 -> t26_1_5 -> t27_2_5 -> t28_3_5 -> t29_3_6 -> t30_3_6 -> t31_3_7 -> t32_2_7 -> t33_1_7 -> t34_1_7 -> t35_0_7 -> t36_1_7 -> t37_2_7 -> t38_2_8 -> t39_2_9 -> t40_1_9 -> t41_0_9 -> t42_1_9 -> t43_1_9 -> t44_0_9 -> t45_0_10 -> t46_0_10 -> t47_0_11 -> t48_0_11 -> t49_1_11 -> t50_1_12 -> t51_1_12 -> t52_2_12 -> t53_2_13 -> t54_2_14 -> t55_2_15 -> t56_2_16 -> t57_2_17 -> t58_2_18 -> t59_3_18 -> t60_3_19 -> t61_3_19 -> t62_3_20 -> t63_3_21 -> t64_3_21 -> t65_3_22 -> t66_3_23 -> t67_2_23 -> t68_1_23 -> t69_0_23 -> t70_0_23 -> t71_0_24 -> t72_0_25 -> t73_0_26 -> t74_0_27 -> t75_0_27 -> t76_0_27 -> t77_0_28 -> t78_0_29 -> t79_0_29 -> t80_1_29 -> t81_1_30 -> t82_1_29 -> t83_1_28 -> t84_1_28 -> t85_1_29 -> t86_0_29 -> t87_0_30 -> t88_1_30 -> t89_1_31 -> t90_1_32 -> t91_0_32 -> t92_0_33 -> t93_0_34 -> t94_0_34 -> t95_0_35 -> t96_1_35 -> t97_0_35 -> t98_0_36 -> t99_1_36 -> t100_1_37 -> t101_1_38 -> t102_1_39 -> t103_2_39 -> t104_2_40 -> t105_3_40 -> t106_4_40 -> t107_5_40 -> t108_5_39 -> t109_6_39 -> t110_6_39 -> t111_5_39 -> t112_4_39 -> t113_4_40 -> t114_4_41 -> t115_4_42 -> t116_4_43 -> t117_4_42 -> t118_5_42 -> t119_6_42 -> t120_6_42 -> t121_6_43 -> t122_6_44 -> t123_6_43 -> t124_6_43 -> t125_6_44 -> t126_6_45 -> t127_5_45 -> t128_5_46 -> t129_6_46 -> t130_6_47 -> t131_7_47 -> t132_8_47 -> t133_8_47 -> t134_8_48 -> t135_7_48 -> t136_6_48 -> t137_5_48 -> t138_5_47 -> t139_5_46 -> t140_5_47 -> t141_5_47 -> t142_5_46 -> t143_6_46 -> t144_6_45 -> t145_6_46 -> t146_6_47 -> t147_6_48 -> t148_7_48 -> t149_8_48 -> t150_8_49 -> t151_8_50 -> t152_8_50 -> t153_8_51 -> t154_8_52 -> t155_7_52 -> t156_7_53 -> t157_6_53 -> t158_6_53 -> t159_6_54 -> t160_6_55 -> t161_6_56 -> t162_7_56 -> t163_7_56 -> t164_7_57 -> t165_7_57 -> t166_6_57 -> t167_5_57 -> t168_4_57 -> t169_4_57 -> t170_4_58 -> t171_4_59 -> t172_4_60 -> t173_4_61 -> t174_4_62 -> t175_5_62 -> t176_5_62 -> t177_5_61 -> t178_5_62 -> t179_6_62 -> t180_6_63 -> t181_7_63 -> t182_7_64 -> t183_7_65 -> t184_6_65 -> t185_6_66 -> t186_5_66 -> t187_6_66 -> t188_6_67 -> t189_5_67 -> t190_5_68 -> t191_5_69 -> t192_5_70 -> t193_5_71 -> t194_6_71 -> t195_6_72 -> t196_5_72 -> t197_5_73 -> t198_5_73 -> t199_4_73 -> t200_5_73 -> t201_5_74 -> t202_5_75 -> t203_5_76 -> t204_5_75 -> t205_5_74 -> t206_5_75 -> t207_5_75 -> t208_5_76 -> t209_4_76 -> t210_4_77 -> t211_4_78 -> t212_3_78 -> t213_2_78 -> t214_1_78 -> t215_1_77 -> t216_1_77 -> t217_1_77 -> t218_0_77 -> t219_0_78 -> t220_0_79 -> t221_0_80 -> t222_0_81 -> t223_1_81 -> t224_1_81 -> t225_1_81 -> t226_0_81 -> t227_0_80 -> t228_1_80 -> t229_1_80 -> t230_2_80 -> t231_2_79 -> t232_3_79 -> t233_3_80 -> t234_3_81 -> t235_3_82 -> t236_3_82 -> t237_3_83 -> t238_3_84 -> t239_3_85 -> t240_4_85 -> t241_4_86 -> t242_4_87 -> t243_4_88 -> t244_4_89 -> t245_3_89 -> t246_3_90 -> t247_3_91 -> t248_3_92 -> t249_4_92 -> t250_4_93 -> t251_4_93 -> t252_4_94 -> t253_4_93 -> t254_3_93 -> t255_3_93 -> t256_3_94 -> t257_2_94 -> t258_2_95 -> t259_2_96 -> t260_3_96 -> t261_3_97 -> t262_3_98 -> t263_3_99 -> t264_4_99 -> t265_4_100 -> t266_4_101 -> t267_3_101 -> t268_3_102 -> t269_4_102 -> t270_4_103 -> t271_3_103 -> t272_4_103 -> t273_4_103 -> t274_4_104 -> t275_4_104 -> t276_5_104 -> t277_5_104 -> t278_6_104 -> t279_7_104 -> t280_7_104 -> t281_8_104 -> t282_8_105 -> t283_8_106 -> t284_8_107 -> t285_9_107 -> t286_10_107 -> t287_11_107 -> t288_11_107 -> t289_11_108 -> t290_12_108 -> t291_12_109 -> t292_12_110 -> t293_12_111 -> t294_12_112 -> t295_12_113 -> t296_12_114 -> t297_11_114 -> t298_11_114 -> t299_11_113 -> t300_11_114 -> t301_11_115 -> t302_11_116 -> t303_11_117 -> t304_12_117 -> t305_12_118 -> t306_12_119 -> t307_12_120 -> t308_12_121 -> t309_12_122 -> t310_12_122 -> t311_11_122 -> t312_12_122 -> t313_12_123 -> t314_11_123 -> t315_11_124 -> t316_10_124 -> t317_10_125 -> t318_9_125 -> t319_9_126 -> t320_9_127 -> t321_9_126 -> t322_9_127 -> t323_10_127 -> t324_11_127 -> t325_11_128 -> t326_11_128 -> t327_11_127 -> t328_12_127 -> t329_13_127 -> t330_13_128 -> t331_14_128 -> t332_14_127 -> t333_15_127 -> t334_15_128 -> t335_15_129 -> t336_15_130 -> t337_15_131 -> t338_15_132 -> t339_15_133 -> t340_15_133 -> t341_15_134 -> t342_16_134 -> t343_16_135 -> t344_16_136 -> t345_16_137 -> t346_16_137 -> t347_16_138 -> t348_16_139 -> t349_15_139 -> t350_15_140 -> t351_16_140 -> t352_16_141 -> t353_17_141 -> t354_18_141 -> t355_18_142 -> t356_18_143 -> t357_18_144 -> t358_18_145 -> t359_18_145 -> t360_17_145 -> t361_17_146 -> t362_17_146 -> t363_16_146 -> t364_15_146 -> t365_15_147 -> t366_15_148 -> t367_16_148 -> t368_16_149 -> t369_17_149 -> t370_17_149 -> t371_18_149 -> t372_19_149 -> end_node      
#step =  373
"""