from osm2networkx import *
import random

class State:

	def __init__(self, node, parent):
		self.node = node
		self.parent = parent


	def __eq__(self, other):
		if isinstance (other, State):
			return self.node['data'].id == other.node['data'].id
		return NotImplemented


def bidirectionalSearch(graph, start, goal):
	if start == goal:
		print "START == GOAL"
		return None

	frontier_0 = [start]
	frontier_1 = [goal]
	explored_0 = []
	explored_1 = []

	num_explored = 0

	while((len(frontier_0)>0 and len(frontier_1)>0)): #judge two frontier intersection
		if(len(frontier_0)>0):
			node_0 = frontier_0.pop()
			explored_0.append(node_0)
		if(len(frontier_1)>0):
			node_1 = frontier_1.pop()
			explored_1.append(node_1)

		for edge in networkx.edges(graph, node_0.node['data'].id):
			child = State(graph.node[edge[1]], node_0)
			if(child not in explored_0) and (child not in frontier_0):
				if (child in frontier_1): 
					print "Goal found, explored: ", num_explored, "\n\n"
					return num_explored
				else: 
					frontier_0.append(child)
				num_explored = num_explored+1

		for edge in networkx.edges(graph, node_1.node['data'].id):
			child = State(graph.node[edge[1]], node_1)
			if(child not in explored_1) and (child not in frontier_1):
				if (child in frontier_0): 
					print "Goal found, explored: ", num_explored, "\n\n"
					return num_explored
				else: 
					frontier_1.append(child)
				num_explored = num_explored+1

	print "No path found, explored: ", num_explored
	num_explored = -1
	return num_explored

"""
The setup
"""

print "\n\n----- 6601 Grad AI: bidirectional Seaching ATLANTA ------\n\n"
only_roads = True
graph = read_osm('atlanta.osm', only_roads)

start_num = random.randint(0, len(graph.nodes()))
stop_num = random.randint(0, len(graph.nodes()))
dest_num = random.randint(0, len(graph.nodes()))

start     = graph.node[graph.nodes()[start_num]]
stop      = graph.node[graph.nodes()[stop_num]]
dest	  = graph.node[graph.nodes()[dest_num]]
print "NUMBER OF NODES: ", len(graph.nodes())
print "NUMBER OF EDGES: ", len(graph.edges())
print "START:           ", start['data'].id
print "STOP :           ", stop['data'].id
print "DEST :           ", dest['data'].id

num0 = bidirectionalSearch(graph, State(start, None), State(stop, None))
num1 = bidirectionalSearch(graph, State(stop, None), State(dest, None))
num2 = bidirectionalSearch(graph, State(dest, None), State(start, None))

print "total :          ", num0 +num1 + num2


