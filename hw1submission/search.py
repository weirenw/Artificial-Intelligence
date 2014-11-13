from osm2networkx import *
import random

"""
Searching a street network using Breadth First Search

REQUIREMENTS:

  networkx: http://networkx.github.io/

REFERENCES:

  [1] Russel, Norvig: "Artificial Intelligene A Modern Approach", 3rd ed, Prentice Hall, 2010

ASSIGNMENT:

  Extend this program to Tridirectional Search.
  Find a path between three starting points.

author: Daniel Kohlsdorf and Thad Starner
"""

"""
The state space in our problem hold:

   1) A node in the street graph
   2) A parent node

"""
class State:

    def __init__(self, node, parent):
        self.node   = node
        self.parent = parent

    def __eq__(self, other):
        if isinstance(other, State):
            return self.node['data'].id == other.node['data'].id
        return NotImplemented

"""
Implements BFS on our GPS data

see [1] Figure 3.11
"""
def bfs(graph, start, goal):
    if start == goal:
        print "START === GOAL"
        return None
    
    frontier = [start]
    explored = []
    num_explored = 0
    while len(frontier) > 0:
       node = frontier.pop(0)

       explored.append(node)
       for edge in networkx.edges(graph, node.node['data'].id):
           child = State(graph.node[edge[1]], node) 
           if (child not in explored) and (child not in frontier):
               # HINT: Goal - Check
               if child == goal:
                   print "Goal found, explored: ", num_explored, "\n\n"
                   return child
               else:
                   frontier.append(child)
               num_explored = num_explored + 1
    print "No path found, explored: ", num_explored

    return None

"""
Backtrack and output your solution
"""
def backtrack(state, graph):
    if state.parent != None:
        print "Node: ", state.node['data'].id
        if len(state.node['data'].tags) > 0:            
            for key in state.node['data'].tags.keys():
                print "       N: ", key, " ", state.node['data'].tags[key]        
              
        for edge in networkx.edges(graph, state.node['data'].id):
            if len(graph.node[edge[1]]['data'].tags) > 0:
                for key in graph.node[edge[1]]['data'].tags:
                    print "       E: ", graph.node[edge[1]]['data'].tags[key]
        backtrack(state.parent, graph)


"""
The setup
"""

print "\n\n----- 6601 Grad AI: Seaching ATLANTA ------\n\n"
only_roads = True
graph = read_osm('atlanta.osm', only_roads)

start_num = random.randint(0, len(graph.nodes()))
stop_num = random.randint(0, len(graph.nodes()))

start     = graph.node[graph.nodes()[start_num]]
stop      = graph.node[graph.nodes()[stop_num]]
print "NUMBER OF NODES: ", len(graph.nodes())
print "NUMBER OF EDGES: ", len(graph.edges())
print "START:           ", start['data'].id
print "STOP :           ", stop['data'].id

state = bfs(graph, State(start, None), State(stop, None))
if state != None:
    backtrack(state, graph)

print "\n\n"
