
import numpy as np

class vertex: #save as array?
	def __init__(self, ID, net_id, position, connections):
		self.ID = ID #sequential number (from 0 to n-1 vertexes)
		self.net_id = net_id
		self.position = position
		self.connections = connections #IDs if adjacent vertexes
		self.edgesIDs = {}

	def add_edgeID(self, v2_id, edgeID):
		self.edgesIDs[v2_id] = edgeID

class edge:
	def __init__(self, ID, net_id, v1_id, v2_id):
		self.ID = ID
		self.net_id = net_id
		self.v1_id = v1_id
		self.v2_id = v2_id

	def set_params(self, a='random', b='dist', n_cars=0): #In __init__ function?
		if a == 'random':
			self.a = (np.random.rand()+0.1)*50 #adjust factor later
		if b == 'dist':
			self.dist = self.calc_dist(networks[self.net_id].vertexes[v1_id].position, networks[self.net_id].vertexes[v2_id].position)
			self.b = self.dist
		elif b == 'random':
			self.b = (np.random.rand()+0.2)*10000 #adjust factor later
		else:
			self.b = b
		if n_cars == 'random':
			self.n_cars = round(np.random.rand()*1000)#adjust factor later
		else:
			self.n_cars = n_cars
		self.weight = self.calc_weight()

	def calc_weight(self): #later adjust function for more realistic simulation
		assert self.a != None
		assert self.b != None
		assert self.n_cars != None
		self.weight = self.a * self.n_cars + self.b

	def calc_dist(self, P1, P2): #to adjust weights of streets to their length
		return np.sqrt(np.sum(np.sq(P1[0] - P2[0]), np.sq(P1[1] - P2[1])))

class net:

	def __init__(self, net_ID, graph, positions): #graph as dictionary like for example: {0: (1,3,4), 1:(0,4), 2:(4), 3:(0,1), 4:(0,1,2,3)}
	#initialize graph
		self.ID = net_ID
		self.graph = graph
		self.n_vertexes = len(self.graph)
		self.vertexes = [] #Als Dictionary?
		for i in range(self.n_vertexes):
			self.vertexes.append(vertex(i, self.ID, positions[i], graph[i]))
		self.edges = [] #Als Dictionary?
		ID = 0
		for v1_id, v1 in enumerate(self.vertexes): #v1_id == v1.ID
			if type(self.graph[v1.ID]) == int:
				self.graph[v1.ID] = [self.graph[v1.ID]]
			for v2_id in self.graph[v1.ID]:
				self.edges.append(edge(ID, self.ID, v1_id, v2_id))
				v1.add_edgeID(v2_id, ID)
				ID += 1
		self.graph_matrix = np.zeros((self.n_vertexes, self.n_vertexes))

	def initialize_weights(self, all_params=None): #vielleicht ändern, vielleicht in __init__
		if all_params == None:
			self.edges[:].set_params()
		else:
			for i, params in enumerate(all_params):
				a, b, n_cars = params
				self.edges[i].set_params(a, b, n_cars)
		self.initialize_matrix()

	def initialize_matrix(self):
		for edge in self.edges:
			self.graph_matrix[edge.v1, edge.v2] = edge.calc_weight()

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

	#def plot(): #should plot the network


#test
graph = {0: (1,3), 1:(0,2,3), 2:(3), 3:(0,1)}
positions = ((100,100), (200,400), (500,350), (400,50))

networks = {}
networks['test'] = net('test', graph, positions)
print(networks['test'].graph, networks['test'].vertexes[0].position, networks['test'].edges[3].v1_id, networks['test'].edges[3].v2_id)
