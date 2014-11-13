from osm2networkx import *
import random
import math
from Queue import PriorityQueue
import csv


class State:

	def __init__(self, node, parent):
		self.node = node
		self.parent = parent

	def __eq__(self, other):
		if isinstance (other, State):
			return self.node['data'].id == other.node['data'].id
		return NotImplemented

def uniformCostSearch(graph, start, goal):
	if start == goal:
		print "start == goal"
		return None
 	
	pq = PriorityQueue();
	pq.put(start,0); """the other args is priority which should be distance"""
	
	dic = {start.node['data'].id:0};

	frontier = [start]
	explored = []
	num_explored = 0

	while len(frontier)>0:
		node = pq.get()
		if (node in frontier):
			frontier.remove(node)

		if (node == goal):
			print "Goal found, explored: ", num_explored, "\n\n"
			return num_explored
		if (node in explored):
			continue
		explored.append(node)
		for edge in networkx.edges(graph, node.node['data'].id):
			child = State(graph.node[edge[1]], node);
			distance = dic[node.node['data'].id] +  math.sqrt(math.pow(node.node['data'].lat - child.node['data'].lat , 2) + math.pow(node.node['data'].lon - child.node['data'].lon , 2));
			if (child not in frontier) and (child not in explored):
				pq.put(child,distance)
				frontier.append(child)
				dic[child.node['data'].id] = distance
			elif child in frontier:
				if(dic[child.node['data'].id] > distance):
					pq.put(child.node['data'].id, distance)
					dic[child.node['data'].id] = distance
			num_explored = num_explored+1
	print "No path found, explored: ", num_explored
	num_explored = -1
	return num_explored


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

def tridirectionalSearch(graph, start, goal, dest):

	frontier_0 = [start]
	frontier_1 = [goal]
	frontier_2 = [dest]
	explored_0 = []
	explored_1 = []
	explored_2 = []

	num_explored = 0

	while((len(frontier_0)>0 or len(frontier_1)>0) or len(frontier_2)>0 ): #judge two frontier intersection
		if len(frontier_0)>0:
			node_0 = frontier_0.pop();
			explored_0.append(node_0);
		if len(frontier_1)>0:
			node_1 = frontier_1.pop();
			explored_1.append(node_1);
		if len(frontier_2)>0:
			node_2 = frontier_2.pop();
			explored_2.append(node_2);


		for edge in networkx.edges(graph, node_0.node['data'].id):
			child = State(graph.node[edge[1]], node_0)
			if(child not in explored_0) and (child not in frontier_0):
				if ((child in frontier_1) or (child in explored_1)) and ((child in frontier_2) or (child in explored_2)): 
					print "Goal found, explored: ", num_explored, "\n\n"
					return num_explored
				else: 
					frontier_0.append(child)
				num_explored = num_explored+1

		for edge in networkx.edges(graph, node_1.node['data'].id):
			child = State(graph.node[edge[1]], node_1)
			if(child not in explored_1) and (child not in frontier_1):
				if ((child in frontier_0) or (child in explored_0)) and ((child in frontier_2) or (child in explored_2)): 
					print "Goal found, explored: ", num_explored, "\n\n"
					return num_explored
				else: 
					frontier_1.append(child)
				num_explored = num_explored+1

		for edge in networkx.edges(graph, node_2.node['data'].id):
			child = State(graph.node[edge[1]], node_2)
			if(child not in explored_2) and (child not in frontier_2):
				if ((child in frontier_0) or (child in explored_0)) and ((child in frontier_1) or (child in explored_1)): 
					print "Goal found, explored: ", num_explored, "\n\n"
					return num_explored
				else: 
					frontier_2.append(child)
	print "No path found, explored: ", num_explored
	num_explored = -1
	return num_explored


"""
The setup
"""

def setup(): 
	print "\n\n----- 6601 Grad AI: uniform/bidirectional/tridirectional Seaching ATLANTA ------\n\n"
	only_roads = True
	graph = read_osm('atlanta.osm', only_roads)

	start_num = random.randint(0, len(graph.nodes()))
	stop_num = random.randint(0, len(graph.nodes()))
	dest_num = random.randint(0, len(graph.nodes()))

	start     = graph.node[graph.nodes()[start_num]]
	stop      = graph.node[graph.nodes()[stop_num]]
	dest      = graph.node[graph.nodes()[dest_num]]
	print "NUMBER OF NODES: ", len(graph.nodes())
	print "NUMBER OF EDGES: ", len(graph.edges())
	print "START:           ", start['data'].id
	print "STOP :           ", stop['data'].id
	print "DEST :           ", dest['data'].id


	num0 = bidirectionalSearch(graph, State(start, None), State(stop, None))
	num1 = bidirectionalSearch(graph, State(stop, None), State(dest, None))
	num2 = bidirectionalSearch(graph, State(dest, None), State(start, None))

	if(num0>=0 and num1>=0 and num2>=0):

		print"bidireationalSearch explored :        ", num0+num1+num2

		num = tridirectionalSearch(graph, State(start, None), State(stop, None), State(dest, None))
		print"tridirectionalSearch explored :        ", num
	
		num_0 = uniformCostSearch(graph, State(start, None), State(stop, None))
		num_1 = uniformCostSearch(graph, State(stop, None), State(dest, None))
		num_2 = uniformCostSearch(graph, State(dest, None), State(start, None))
		print"uniformCostSearch explored :        ", num_0 + num_1 + num_2

		resultFile =  open('result.csv', 'a')
		data = [num0+num1+num2, num, num_0 + num_1 + num_2]
		wr = csv.writer(resultFile, dialect='excel')
		wr.writerow(data)
		return True
	else: 
		return False

resultFile =  open('result.csv', 'a')
data = ['bidirectionalSearch', 'tridirectionalSearch', 'UniformSearch']
wr = csv.writer(resultFile, dialect='excel')
wr.writerow(data)
num = 0
while(num<110):
	if setup():
		num+=1




