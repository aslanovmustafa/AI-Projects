from copy import deepcopy
import numpy as np
import pandas as pd

def graph():
  edges, nodes = [], []
  with open("2.txt",'r') as filename: #specify text format here
    for line in filename.readlines(): 
      if not line.startswith("#"):
        if line.startswith("colors" or "Colors"):
          cnum = int(line.split('=')[1])
        elif not line.strip(): continue
        else:
          v1 = line.split(',')[0]
          v2 = line.split(',')[1].replace("\n","")
          edges.append((v1,v2))
          nodes.append(v1)
          nodes.append(v2)
  nodes = list(set(nodes))
  return nodes,edges, cnum

def is_complete(result, nodes): #just fucntion to check if the solution is complete or not
  if len(result)==len(nodes): return True
  else: return False

def f_u_v(result, nodes, domains, constraints): #checks for the first unassigned node in the selected list
    unassigned_nodes = [x for x in nodes if x not in result]
    node = unassigned_nodes[0]
    return node

def s_d_c(variable, result, nodes, domains, constraints): #function that returns the value in a static ordering
    for domain_value in domains[variable]:
        yield domain_value

def value_consistency(node, value, result, constraints):
    if result is None: return False
    for v in constraints:
        if v in result:
            if value is result[v]:
                return False
    return True

def avoid_loop(nodes, domains, constraints, node, value, result): #this function is not doing much but letting me to avoid the loop in the backtracking. I know it's hardcoding but i can't help it at the moment
    return True

def backtrack(result, nodes, domains, constraints, heuristics): #eventually where the backtracking happens
    if is_complete(result, nodes): return True, result
    node = f_u_v(result, nodes, domains, constraints)
    for value in s_d_c(node, result, nodes, domains, constraints):
        if value_consistency(node, value, result, constraints[node]):
            result[node], m_csp = value, deepcopy(nodes, domains, constraints) #A deep copy constructs a new compound object and then, recursively, inserts copies into it of the objects found in the original
            if avoid_loop(nodes, domains, constraints, node, value, result):
                check, result = backtrack(deepcopy(result), nodes, domains, constraints, heuristics)
                if check: return True, result
            del result[node]
            (nodes, domains, constraints) = m_csp
    return False, result

def backtracking_search(nodes, domains, constraints, heuristics): #using this reference function help avoiding maximum recursion depth error
    result = dict()
    return backtrack(result, nodes, domains, constraints, heuristics)

def adj_list(nodes, edges): #just creates and adjacent list from given nodes and edges
    adjacency_list = dict()
    for node in nodes:
        aList = set()
        [aList.add(x) for x, y in edges if x != node and y == node]
        [aList.add(y) for x, y in edges if y != node and x == node]
        adjacency_list[node] = aList
    return adjacency_list

def mrv(result, nodes, domains, constraints): #minimum remaining value
    unassigned_nodes = [x for x in nodes if x not in result]
    node_domain_count = [(x, len(domains[x])) for x in unassigned_nodes]
    nodes = sorted(node_domain_count, key=itemgetter(1))
    return nodes[0][0]

def lcv(node, result, nodes, domains, constraints): #least constraining value
    neighbors = constraints[node]
    value_count = []
    for value in domains[node]:
        count = 0
        for neighbor in neighbors:
            if value in domains[neighbor]:
                count = count + 1
        value_count.append((value, count))
    counted = sorted(value_count, key=itemgetter(1), reverse=True)
    for value, count in counted:
        yield value

palette = ["red", "orange", "yellow", "green", "blue",  "purple"]
def color_graph(graph, heuristics=(mrv, lcv)):
    colors, nodes, constraints = palette[0:graph[2]], graph[0], adj_list(graph[0], graph[1])
    domains = dict([(x, colors) for x in nodes])
    result = backtracking_search(nodes, domains, constraints, heuristics)
    if not result: print("Can't solve it :(")
    else: 
      for key, value in result[1].items():
        print("Vertex",key, '- color:', value)

color_graph(graph())