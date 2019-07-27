 import numpy as np #necessary with packages?

class vertex: #save as array?
	def __init__(self, ID, position, connections):
		self.ID = ID #sequential number (from 0 to n-1 vertexes)
		self.position = position
		self.connections = connections #probably not necessary because it is included in self.edges
		self.edges = {}

	def add_edge(self, edge):
		self.edges[edge.v2] = edge

class edge:
	def __init__(self, ID, v1, v2):
		self.ID = ID
		self.v1 = v1
		self.v1 = v2
		self.dist = self.calc_dist(self.v1.position, self.v2.position)

	def set_params(self, a, b=self.dist, n_cars=0): #In __init__ function?
		self.a = a
		self.b = b
		self.n_cars = n_cars
		self.weight = self.calc_weight(self.a)

	def calc_weight(self): #later adjust function for more realistic simulatuin
		self.weight = self.a * self.n_cars + self.b

	def calc_dist(P1, P2): #to adjust weights of streets to their length
		return np.sqrt(np.sum(np.sq(P1[0] - P2[0]), np.sq(P1[1] - P2[1])))

class net:

	def __init__(self, graph, positions): #graph as dictionary like for example: {0: (1,3,4), 1:(0,4), 2:(4), 3:(0,1), 4:(0,1,2,3)}
	#initialize graph
		self.graph = graph
		self.n_vertexes = len(graph)
		self.vertexes = np.zeros((n_vertexes))
		for i in range(n_vertexes):
			self.vertexes[i] = vertex(i, positions[i], graph[i])
		self.n_edges = np.sum((len(self.graph[x]) for x in self.graph)) #Anzahl Kanten
		self.edges = mp.zeros((n_edges))
		ID = 0
		for v1 in vertexes:
			for v2 in graph[v1.ID]:
				self.edges[ID] = edge(ID, v1.ID, v2)
				v1.add_edge(self.edges[ID])
				ID += 1
		self.graph_matrix = np.zeros((n_vertexes, n_vertexes))

	def initialize_weights(self, weights):
		####todo: initialize weights to edges with edge.set_params
		self.initialize_matrix()


	######car management################connect to class car later########
	def add_car(self, edge, num=1):
		edge.n_cars += num
		edge.calc_weight()
		self.graph_matrix[edge.v1.ID, edge.v2.ID] = edge.weight

	def remove_car(self, edge, num=1):
		edge.n_cars -= num
		edge.calc_weight()
		self.graph_matrix[edge.v1.ID, edge.v2.ID] = edge.weight
	######################################

	def initialize_matrix(self):
		for edge in self.edges:
			self.graph_matrix[edge.v1, edge.v2] = edge.calc_weight()

	#def plot(): #should plot the network


#test
graph = {0: (1,3), 1:(0,2,3), 2:(3), 3:(0,1)}
positions = ((100,100), (200,400), (500,350), (400,50))

