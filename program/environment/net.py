
import numpy as np

class Vertex: #Stellt die Knoten im Netzwerk dar
	def __init__(self, ID, position, connections):
		self.ID = ID #Einfach eine sequenzielle Zahl; Der Index im Array network.vertexes
		self.position = position #Koordinaten
		self.connections = connections #Die IDs der Knoten, zu denen dieser Knoten direkt führt
		self.edgesIDs = {} #Die IDs der Kanten, die von dem Knoten ausgehen

	def add_edgeID(self, v2_id, edgeID):
		self.edgesIDs[v2_id] = edgeID

class Edge: #Stellt die Kanten im Netzwerk dar
	def __init__(self, ID, v1_id, v2_id, a, b, n_cars=0):
		self.ID = ID
		self.v1_id = v1_id #Startknoten
		self.v2_id = v2_id #Endknoten
		#Konstante Gewichtsparameter
		self.a = a
		self.b = b
		#Anzahl der Autos auf der Kante
		self.n_cars = n_cars
		self.calc_weight()

	def calc_weight(self): #später weiter präzisieren
		self.weight = round(self.a * self.n_cars + self.b)

	def calc_dist(self, P1, P2): #Die Länge im Koordinatensystem #vielleicht nützlich für die automatische Generierung später
		return np.sqrt(np.sum(np.sq(P1[0] - P2[0]), np.sq(P1[1] - P2[1])))

class Net:#Stellt das Netzwerk dar
	def __init__(self, positions, data_a, data_b): #Initiert das Netzwerk #Eingabe als mehrere konstante Matrizen
		self.fixed_params = [positions, data_a, data_b] #vermutlich nicht nötig
		n_vertexes = np.shape(positions)[0]
		self.vertexes = [] #Liste der Knoten
		for i in range(n_vertexes):
			connections = []
			for j, relation in enumerate(data_a[i]):
				if relation != 0:
					connections.append(j)
			self.vertexes.append(Vertex(i, positions[i], connections))
		self.edges = [] #Liste der Kanten
		edge_nr = 0
		for i in range(n_vertexes):
			for j in range(n_vertexes):
				if data_a[i, j] != 0:
					self.edges.append(Edge(edge_nr, i, j, data_a[i, j], data_b[i, j]))
					self.vertexes[i].add_edgeID(j, edge_nr)
					edge_nr += 1
		self.graph_matrix = np.zeros((n_vertexes, n_vertexes)) #Variable Matrix
		for edge in self.edges:
			self.graph_matrix[edge.v1_id, edge.v2_id] = edge.weight

	#Netzwerk anpassen, wenn ein Auto auf eine Kante kommt
	def add_car(self, edge_ID, num=1):
		edge = self.edges[edge_ID]
		edge.n_cars += num
		edge.calc_weight()
		self.graph_matrix[edge.v1_id, edge.v2_id] = edge.weight

	#Netzwerk anpassen, wenn ein Auto eine Kante verlässt
	def remove_car(self, edge_ID, num=1):
		edge = self.edges[edge_ID]
		edge.n_cars -= num
		edge.calc_weight()
		self.graph_matrix[edge.v1_id, edge.v2_id] = edge.weight


def initialize_network(positions, data_a, data_b):#initiert das Netzwerk
	global network
	network = Net(positions, data_a, data_b)

