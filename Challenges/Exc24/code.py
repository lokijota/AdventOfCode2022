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
with open('Challenges\Exc24\input_debug.txt') as f:
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
        graph = {}
        for node in nodes:
            graph[node] = {}
        
        graph.update(init_graph)
        
        for node, edges in graph.items():
            for adjacent_node, value in edges.items():
                if graph[adjacent_node].get(node, False) == False:
                    graph[adjacent_node][node] = value
                    
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

####################### fim da implementação de grafo

# set useful variables. note I'm excluding the outer walls from the coordinate system to simplify math operations
height = len(lines)-2
width = len(lines[0])-2
start_pos = (-1, 0)
end_pos = (width, height)

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

def print_map(blizzards, width, height):
    map = np.full((width,height), ".")

    for blizzard in blizzards:
        map[blizzard[0], blizzard[1]] = blizzard[2]

    for row in map:
        for col in row:
            if col in ['<', '>', '^', 'v']:
                print(colored(col, 'red'), end='')
            else:
                print(col, end='')
        print()

print_map(blizzards_at_start, width, height)
print(free_positions_at_minute(blizzards_at_start, 1, width, height))
