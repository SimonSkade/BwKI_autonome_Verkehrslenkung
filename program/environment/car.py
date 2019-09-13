from . import net
import numpy as np

graph_matrix = net.network.graph_matrix
vertexes = net.network.vertexes

class Car: #Objekte von Car stellen Autos dar
	def __init__(self, ID, start_node_ID, end_node_IDs, init_with_djikstra=True):
		self.ID = ID
		self.start_node_ID = start_node_ID
		self.end_node_IDs = end_node_IDs #Ist eine Liste!, auch wenn es meistens nur ein Element enthält
		self.edge_ids = []
		if init_with_djikstra:
			self.create_with_djikstra()
		
	def create_with_djikstra(self):
		for i in range(len(self.end_node_IDs) - 1, 0, -1): #Pfade von Zwischenknoten zum Endknoten berechnen
			self.djikstra(self.end_node_IDs[i-1], self.end_node_IDs[i])
		self.djikstra(self.start_node_ID, self.end_node_IDs[0])# Pfad von Startknoten zum (ersten) Endknoten berechnen
		self.actual_edge = self.edge_ids[0]
		self.future_edge_IDs = self.edge_ids[1:]

	def djikstra(self, start_node_ID, end_node_ID): #berechnet den schnellsten Pfad und speichert die zukünftig abgefahrenen Kanten
		num_nodes = len(vertexes)
		actual_node_ID = start_node_ID
		actual_node_value = 0
		predecessor = np.zeros((num_nodes), dtype='int32')
		unvisited = {}
		for node in	range(num_nodes):
			if node != start_node_ID:
				unvisited[node] = float("Inf")
		for i, weight in enumerate(graph_matrix[actual_node_ID]):
			if weight != 0:
				unvisited[i] = weight
				predecessor[i] = actual_node_ID
		while unvisited:
			min_node_value = float("Inf")
			for key, value in unvisited.items():
				if value < min_node_value:
					min_node_value = value
					actual_node_ID = key
					actual_node_value = value
			try:
				del unvisited[actual_node_ID]
			except KeyError:
				raise Exception("Das generierte Netzwerk war leider nicht zusammenhängend, bitte probiere es erneut!")
			if actual_node_ID == end_node_ID:
				break
			for connecting_node_id, weight in enumerate(graph_matrix[actual_node_ID]):
				if weight != 0:
					if connecting_node_id in unvisited:
						potential_node_value = actual_node_value + weight
						if potential_node_value < unvisited[connecting_node_id]:
							unvisited[connecting_node_id] = potential_node_value
							predecessor[connecting_node_id] = actual_node_ID
		while actual_node_ID != start_node_ID:
			node_before = vertexes[predecessor[actual_node_ID]]
			self.edge_ids.insert(0, node_before.edgesIDs[actual_node_ID])
			actual_node_ID = node_before.ID

	def step(self, edge_id):
		done = False
		reward = -1
		self.edge_ids.append(edge_id)
		next_node_id = net.network.edges[edge_id].v2_id
		next_state = calc_state(next_node_id, self.end_node_IDs[0])
		if next_node_id == self.end_node_IDs[0]:
		    done = True
		    reward = 50
		    del self.end_node_IDs[0]
		    next_state = None
		    if self.end_node_IDs:
		        next_state = calc_state(next_node_id, self.end_node_IDs[0])
		return next_state, done, reward

	def set_params(self, edge_ids):
		self.edge_ids = edge_ids
		self.actual_edge = self.edge_ids[0]
		self.future_edge_IDs = self.edge_ids[1:]

def calc_state(actual_node_id, end_node_id):
    input_edge_array = np.zeros((len(net.network.edges)))
    possible_edge_ids = [net.network.vertexes[actual_node_id].edgesIDs[x] for x in net.network.vertexes[actual_node_id].connections]
    for edge_id in possible_edge_ids:
        input_edge_array[edge_id] = net.network.edges[edge_id].weight
    input_node_array = np.zeros((len(net.network.vertexes)))
    input_node_array[end_node_id] = 1
    return np.concatenate((input_edge_array, input_node_array))




