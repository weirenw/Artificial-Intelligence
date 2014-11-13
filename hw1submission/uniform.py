from osm2networkx import *
import random
import math
from Queue import PriorityQueue

class MyPriorityQueue(PriorityQueue):
	def __init__(self):
		PriorityQueue.__init(self)
		self.counter = 0

	def put(self, item, priority):
		PriorityQueue.put(self, (priority, self.counter, item))
		self.counter += 1

	def get(self, *args, **kwargs):
   	        _, _, item = PriorityQueue.get(self, *args, **kwargs)
		return item



class State:

	def __init__(self, node, parent):
		self.node = node
		self.parent = parent

	def __eq__(self,other):
		if isinstance(other, State):
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
"""
The setup
"""

print "\n\n----- 6601 Grad AI: Unifort cost Seaching ATLANTA ------\n\n"
only_roads = True
graph = read_osm('atlanta.osm', only_roads)

start_num = random.randint(0, len(graph.nodes()))
stop_num_0 = random.randint(0, len(graph.nodes()))
stop_num_1 = random.randint(0, len(graph.nodes()))

start     = graph.node[graph.nodes()[start_num]]
stop_0      = graph.node[graph.nodes()[stop_num_0]]
stop_1 = graph.node[graph.nodes()[stop_num_1]]

print "NUMBER OF NODES: ", len(graph.nodes())
print "NUMBER OF EDGES: ", len(graph.edges())
print "START:           ", start['data'].id
print "STOP_0:          ", stop_0['data'].id
print "STOP_1:          ", stop_1['data'].id

num_0 = uniformCostSearch(graph, State(start, None), State(stop_0, None))
num_1 = uniformCostSearch(graph, State(stop_0, None), State(stop_1, None))
num_2 = uniformCostSearch(graph, State(stop_1, None), State(start, None))
num = num_0 + num_1 + num_2
print "total number explored: ", num, "\n\n"
print "\n\n"



