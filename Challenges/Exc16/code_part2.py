import re
import numpy as np
from operator import itemgetter
import anytree
import sys
import itertools
from timeit import default_timer as timer

maxroi = 0
dijkstra_cache = {}

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

    # jota: look for cache hit
    if start_node in dijkstra_cache:
        return dijkstra_cache[start_node][0], dijkstra_cache[start_node][1]

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
    
    # jota - load the cache
    dijkstra_cache[start_node] = (previous_nodes, shortest_path)

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

def build_distance_dictionary(graph, nodes):
    distances = {}
    for source_node in nodes + ["AA"]:
        previous_nodes, shortest_path = dijkstra_algorithm(graph=graph, start_node=source_node)
        for target_node in nodes:
            if source_node != target_node:
                best_path = get_path(previous_nodes, source_node, target_node)
                distances[source_node+target_node] = len(best_path) - 1
    return distances

##################### Tree representation for A*-like algorithm

class TreeNode(anytree.NodeMixin):
    def __init__(self, valve1, roi1, elapsed1, valve2, roi2, elapsed2, unvisited_valves, parent=None, children=None):
        self.e1_valve = valve1
        self.e1_roi = roi1
        self.e1_elapsed_ticks = elapsed1

        self.e2_valve = valve2
        self.e2_roi = roi2
        self.e2_elapsed_ticks = elapsed2

        # o roi pode ser só um campo
        self.unvisited_valves = unvisited_valves
        
        self.parent = parent
        if children:  # set children only if given
            self.children = children

def print_tree(top_node):
    for pre, fill, node in anytree.RenderTree(top_node):
        treestr = u"%s%s" % (pre, node.e1_valve + "|" + node.e2_valve)
        print(treestr.ljust(8), node.e1_roi, node.e1_elapsed_ticks, "|", node.e2_roi, node.e2_elapsed_ticks)

def print_tree_ascending(node):

    text_file = open("log.txt", "a")

    treestr = u"%s%s" % (" [ ", node.e1_valve + "|" + node.e2_valve)
    print(treestr.ljust(7), node.e1_roi, node.e1_elapsed_ticks, "|", node.e2_roi, node.e2_elapsed_ticks)
    text_file.write(treestr.ljust(7) + str(": ") +  str(node.e1_roi) + " " +str(node.e1_elapsed_ticks) + "|" + str(node.e2_roi) + " " + str(node.e2_elapsed_ticks) + "\n")

    while node.parent != None:
        node = node.parent
        treestr = u"%s%s" % ("<- ", node.e1_valve + "|" + node.e2_valve)
        print(treestr.ljust(7), node.e1_roi, node.e1_elapsed_ticks, "|", node.e2_roi, node.e2_elapsed_ticks)
        text_file.write(treestr.ljust(7) + str(": ") + str(node.e1_roi) + " " +str(node.e1_elapsed_ticks) + "|" + str(node.e2_roi) + " " + str(node.e2_elapsed_ticks) + "\n")
    
    text_file.write("\n")
    text_file.flush()
    text_file.close()

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

# dict auxiliar para guardar os valores de flow_rate de cada válvula
flow_rates = {node:flow_rate for node, flow_rate, _ in valves}

graph = Graph(list(map(itemgetter(0), valves)), init_graph)

def calculate_roi(start_node, end_node, time_remaining):
    ticks_to_get_there = distances[start_node+end_node]
    # returns [roi, elapsed_ticks]
    return [flow_rates[end_node]*(time_remaining - ticks_to_get_there -1), ticks_to_get_there+1] # includes the tick to activate
            
### AQUI É QUE ISTO SE TORNA SÉRIO

def generate_children_v2(tree_node, level=1):
    global maxroi
    global distances

    # gerar todas as combinações possíveis de válvulas para os dois elefantes a partir das posições actuais
    # assume que há um número >= 2 de válvulas não visitadas
    combinations = list(itertools.combinations(tree_node.unvisited_valves, 2))
    combinations += [(combination[1], combination[0]) for combination in list(combinations)]
    # combinations = [('BB', 'CC'), ('BB', 'DD'), ...

    if level > 3:
        # add the option of "staying put" as possible movements
        e1_doesnt_move = [(tree_node.e1_valve, node) for node in tree_node.unvisited_valves]
        e2_doesnt_move = [(node, tree_node.e2_valve) for node in tree_node.unvisited_valves]
        combinations += e1_doesnt_move + e2_doesnt_move

    # prune longer distances
    if level <= 2:
        # combinations = [x for d, x in zip([distances[c[1] + c[0]] for c in combinations], combinations) if d <= 10]
        # combinations = [x for d, x in sorted(zip([distances[c[1] + c[0]] for c in combinations], combinations)) if d <= 10]
        combinations = [x for d, x in sorted(zip([distances[c[1] + c[0]] for c in combinations], combinations))]
        # print("At level ", level, " combinations: ", combinations)

    # agora, como antes, calcular o ROI de cada combinação, para podermos criar o nó da árvore
    # começamos com o e1
    # obsolete - previous_nodes, shortest_path = dijkstra_algorithm(graph=graph, start_node=tree_node.e1_valve)
    rois_unvisited_valve_e1 = { valve_name:calculate_roi(tree_node.e1_valve, valve_name, 26-tree_node.e1_elapsed_ticks) for valve_name in tree_node.unvisited_valves}

    # small optimization, but I should be keeping all of these in a cache NOTAJOTA
    if tree_node.e1_valve != tree_node.e2_valve: 
        # obsolete - previous_nodes, shortest_path = dijkstra_algorithm(graph=graph, start_node=tree_node.e2_valve)
        rois_unvisited_valve_e2 = { valve_name:calculate_roi(tree_node.e2_valve, valve_name, 26-tree_node.e2_elapsed_ticks) for valve_name in tree_node.unvisited_valves}
    else: # se é o mesmo...
        rois_unvisited_valve_e2 = rois_unvisited_valve_e1

    # criar um nó novo para cada par de válvulas visitados pelos elefantes, recorrendo às combinações geradas acima
    for combination in combinations:

        # prune the tree during the initial levels
        if level < 3 and (combination[0] in ('FL', 'OL', 'CS', 'UK') or combination[1] in ('FL', 'OL', 'CS', 'UK')):
            continue

        # calcular o ROI de cada combinação
        rois_unvisited_valve_e1[tree_node.e1_valve] = [0, 0]
        rois_unvisited_valve_e2[tree_node.e2_valve] = [0, 0]

        roi_e1 = tree_node.e1_roi + rois_unvisited_valve_e1[combination[0]][0]
        roi_e2 = tree_node.e2_roi + rois_unvisited_valve_e2[combination[1]][0]
        if roi_e1 > 0 and roi_e2 > 0: # else skip, no point in adding paths with negative return
            # calcular o tempo de viagem de cada elefante
            e1_elapsed_ticks = tree_node.e1_elapsed_ticks + rois_unvisited_valve_e1[combination[0]][1]
            e2_elapsed_ticks = tree_node.e2_elapsed_ticks + rois_unvisited_valve_e2[combination[1]][1]
            
            if e1_elapsed_ticks > 26 or e2_elapsed_ticks > 26:
                continue

            # remover os nós que vamos visitar da lista de nós não visitados
            remaining_valves = tree_node.unvisited_valves.copy()

            if combination[0] in remaining_valves:
                remaining_valves.remove(combination[0])
            if combination[1] in remaining_valves:
                remaining_valves.remove(combination[1])
            
            # criar o nó
            new_node_roi = roi_e1 + roi_e2
            new_node = None

            if ((level == 1 and (new_node_roi > 450)) or level > 1 ): #or \
            #     (level == 2 and new_node_roi > 500) or \
            #     (level == 3 and new_node_roi > 1600):

                if len(remaining_valves) > 0:
                    new_node = TreeNode(combination[0], roi_e1, e1_elapsed_ticks, combination[1], roi_e2, e2_elapsed_ticks, remaining_valves, parent=tree_node)
                    
            if new_node_roi > maxroi:
                maxroi = new_node_roi
                text_file = open("log.txt", "a")
                text_file.write("\nNew max ROI:" + str(maxroi) + " found on level " + str(level) + "\n")
                text_file.flush()
                text_file.close()

                print("New max ROI:", maxroi, "found on level ", level)
                # print_tree(tree_node)
                if new_node is not None:
                    print_tree_ascending(new_node)
                else:
                    print_tree_ascending(tree_node)


    # caso especial -- só há um nó não visitado. neste caso não vamos entrar no loop acima sequer, só temos de ver o caso
    # de cada elefante ir para o mesmo nó à vez (apenas um)
    if len(tree_node.unvisited_valves) == 1:

        # .............................
        # NOTAJOTA -- ISTO SÓ É RELEVANTE SE AINDA HOUVER TEMPO!! O ROI PODE SER NEGATIVO, AFINAL DE CONTAS, AO CHEGAR AQUI *****
        # .............................


        # agora, como antes, calcular o ROI de cada combinação, para podermos criar o nó da árvore
        # começamos com o e1
        # obsolete - previous_nodes, shortest_path = dijkstra_algorithm(graph=graph, start_node=tree_node.e1_valve)
        rois_unvisited_valve_e1 = calculate_roi(tree_node.e1_valve, tree_node.unvisited_valves[0], 26-tree_node.e1_elapsed_ticks)
        
        # obsolete - previous_nodes, shortest_path = dijkstra_algorithm(graph=graph, start_node=tree_node.e2_valve)
        rois_unvisited_valve_e2 = calculate_roi(tree_node.e2_valve, tree_node.unvisited_valves[0], 26-tree_node.e2_elapsed_ticks)
        
        # calcular o ROI de cada combinação
        roi_if_e1_moves = tree_node.e1_roi + tree_node.e2_roi + rois_unvisited_valve_e1[0] 
        roi_if_e2_moves = tree_node.e1_roi + tree_node.e2_roi + rois_unvisited_valve_e2[0] 

        if roi_if_e1_moves > maxroi:
            maxroi = roi_if_e1_moves
            print("New max ROI:", maxroi, "found on level ", level)
        elif roi_if_e2_moves > maxroi:
            maxroi = roi_if_e2_moves
            print("New max ROI:", maxroi, "found on level ", level)

        # é nó terminal, por isso não vamos criar o TreeNode

    for child in tree_node.children:
        generate_children_v2(child, level+1)

    # if we got here we're close to finishing to lets free up the objects
    tree_node.children = []

    return


# generate all he possible paths starting from AA and add them to the tree
valves_worth_visiting = [node for node in graph.get_nodes() if flow_rates[node] > 0]
tree = TreeNode('AA', 0, 0, 'AA', 0, 0, valves_worth_visiting)
maxroi = 0
distances = build_distance_dictionary(graph, valves_worth_visiting)

start = timer()

generate_children_v2(tree)
# print("ROI:", max([node.e1_roi+node.e2_roi for node in anytree.PreOrderIter(tree)]))
print("Final max ROI:", maxroi)

end = timer()
print("Elapsed time:", end - start)



# possible prunning:
# {'BB': [363, 2], 'CC': [52, 3], 'DD': [559, 2], 'EE': [79, 3], 'HH': [523, 6], 'JJ': [565, 3]} 
# --> HH has high return but many steps (max steps?)
# --> several of them have low yeld or low yeld per step --> drop? but depends on how early we are in the game

# print_tree(tree)



w = anytree.Walker()

for node in anytree.PreOrderIter(tree):
    
    if node.e1_roi + node.e2_roi == maxroi:
        print("**")
        max = node.e1_roi + node.e2_roi

        the_walk = w.walk(node, tree)
        path = list(the_walk[0])
        path.append(the_walk[1])
        path.reverse()
        
        for walknode in path:
            print(walknode.e1_valve, "(", walknode.e1_roi, walknode.e1_elapsed_ticks, ")", walknode.e2_valve, "(", walknode.e2_roi, walknode.e2_elapsed_ticks, ")",end=" / ")