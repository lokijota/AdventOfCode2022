import re
import numpy as np
from operator import itemgetter
import anytree
import sys

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

def get_path(prev_nodes, start_node, target_node):
    path = []
    node = target_node
    
    while node != start_node:
        path.append(node)
        node = prev_nodes[node]
 
    # Add the start node manually
    path.append(start_node)
    path.reverse()
    return path

##################### Tree representation for A*-like algorithm

class TreeNode(anytree.NodeMixin):
    def __init__(self, valve, elapsed_ticks, roi, unvisited_valves, parent=None, children=None):
        self.valve = valve
        self.elapsed_ticks = elapsed_ticks
        self.roi = roi
        self.unvisited_valves = unvisited_valves
        self.parent = parent
        if children:  # set children only if given
            self.children = children

def print_tree(top_node):
    for pre, fill, node in anytree.RenderTree(top_node):
        treestr = u"%s%s" % (pre, node.valve)
        print(treestr.ljust(8), node.roi, node.elapsed_ticks)

# ler todas as linhas, como de costume
with open('Challenges\Exc16\input.txt') as f:
    lines = f.read().splitlines()

# extrair a informação relevante com uma regex, e depois fazer as conversões necessárias para o tipo de dados que quero
# eg - [['AA', 0, ['DD', 'II', 'BB']], ['BB', 13, ['CC', 'AA']], ['CC', 2, ['DD', 'BB']], ['DD', 20, ['CC', 'AA', 'EE']], ['EE', 3, ['FF', 'DD']], ['FF', 0, ['EE', 'GG']], ['GG', 0, ['FF', 'HH']], ['HH', 22, ['GG']], ['II', 0, ['AA', 'JJ']], ['JJ', 21, ['II']]]
regex = "^Valve ([A-Z]{2}) has flow rate=(\d+); tunnel[s]? lead[s]? to valve[s]? ([A-Z]{2}(?:, [A-Z]{2})*)$"
valves = [re.findall(regex, line) for line in lines]
valves = [[valve[0][0], int(valve[0][1]), list(map(lambda x: x.strip(), valve[0][2].split(",")))] for valve in valves]

# criar um grafo com os dados lidos
init_graph = {node:{} for node in list(map(itemgetter(0), valves))}

for valve in valves:
    for connected_valve in valve[2]:
        init_graph[valve[0]][connected_valve] = 1
# print(init_graph)

# dict auxiliar para guardar os valores de flow_rate de cada válvula
flow_rates = {node:flow_rate for node, flow_rate, _ in valves}
# print(flow_rates)

graph = Graph(list(map(itemgetter(0), valves)), init_graph)
# print(graph.graph)

# print(get_path(previous_nodes, start_node="AA", target_node="CC"))
def calculate_roi(start_node, end_node, time_remaining, previous_nodes):
    best_path = get_path(previous_nodes, start_node, end_node)
    ticks_to_get_there = len(best_path) - 1
    return [flow_rates[end_node]*(time_remaining - ticks_to_get_there -1 ), ticks_to_get_there+1] # includes the tick to activate
            
### AQUI É QUE ISTO SE TORNA SÉRIO

# função para gerar a árvore
def generate_children(tree_node): # eg se AA

    # calculate best paths to all the unvisited valves
    previous_nodes, shortest_path = dijkstra_algorithm(graph=graph, start_node=tree_node.valve)
    valves_visit_roi = { valve_name:calculate_roi(tree_node.valve, valve_name, 30-tree_node.elapsed_ticks, previous_nodes) for valve_name in tree_node.unvisited_valves}
    # print(valves_visit_roi)

    # create a new node for each unvisited valve/roi
    for roikey in valves_visit_roi.keys():
        remaining_valves = tree_node.unvisited_valves.copy()
        remaining_valves.remove(roikey)
        if valves_visit_roi[roikey][0] > 0: #else skip, no point in adding paths with negative return
            new_node = TreeNode(roikey, tree_node.elapsed_ticks + valves_visit_roi[roikey][1], tree_node.roi + valves_visit_roi[roikey][0], remaining_valves, parent=tree_node)

    # now generate the next level of the tree
    # print_tree(tree)

    for child in tree_node.children:
        generate_children(child)

    return

# generate all he possible paths starting from AA and add them to the tree
valves_worth_visiting = [node for node in graph.get_nodes() if flow_rates[node] > 0]
# previous_nodes = {} # global variable / don't delete
# shortest_path = {} # global variable / don't delete
# # previous_nodes, shortest_path = dijkstra_algorithm(graph=graph, start_node="AA")

# valves_visit_roi = {valve_name:calculate_roi("AA", valve_name, 30) for valve_name in valves_worth_visiting}
# print(valves_visit_roi) #{'BB': 363, 'CC': 52, 'DD': 559, 'EE': 79, 'HH': 523, 'JJ': 565}

tree = TreeNode('AA', 0, 0, valves_worth_visiting)
generate_children(tree)

# possible prunning:
# {'BB': [363, 2], 'CC': [52, 3], 'DD': [559, 2], 'EE': [79, 3], 'HH': [523, 6], 'JJ': [565, 3]} 
# --> HH has high return but many steps (max steps?)
# --> several of them have low yeld or low yeld per step --> drop? but depends on how early we are in the game

# print_tree(tree)


print(max([node.roi for node in anytree.PreOrderIter(tree)]))

max = 1600
w = anytree.Walker()

for node in anytree.PreOrderIter(tree):
    
    if node.roi > max:
        print("**")
        max = node.roi

        the_walk = w.walk(node, tree)
        path = list(the_walk[0])
        path.append(the_walk[1])
        path.reverse()
        
        for walknode in path:
            print(walknode.valve, "(", walknode.roi, walknode.elapsed_ticks, ")", end=" / ")