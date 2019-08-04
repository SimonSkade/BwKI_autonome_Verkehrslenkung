from . import net
import numpy as np

graph_matrix = net.network.graph_matrix
vertexes = net.network.vertexes

class Car:
	def __init__(self, ID, start_node_ID, end_node_IDs, edge_IDs=None):
		self.ID = ID
		self.start_node_ID = start_node_ID
		self.end_node_IDs = end_node_IDs #typically just one node; is a tuple
		self.future_edge_ids = []
		# if len(self.end_node_IDs) == 1:
		# 	self.djikstra(self.start_node_ID, self.end_node_IDs[0])
		# else:
		for i in range(len(self.end_node_IDs) - 1, 0, -1):
			self.djikstra(self.end_node_IDs[i-1], self.end_node_IDs[i])
		self.djikstra(self.start_node_ID, self.end_node_IDs[0])
		self.actual_edge = self.future_edge_ids[0]
		self.future_edge_IDs = self.future_edge_ids[1:]

	def djikstra(self, start_node_ID, end_node_ID): #calculates shortest path and sets self.future_edge_ids
		num_nodes = graph_matrix.shape[0]
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
			del unvisited[actual_node_ID]
			if actual_node_ID == end_node_ID:
				break
			for connecting_node_id, weight in enumerate(graph_matrix[actual_node_ID]):
				if weight != 0:
					if connecting_node_id in unvisited:
						potential_node_value = actual_node_value + weight
						if potential_node_value < unvisited[connecting_node_id]:
							unvisited[connecting_node_id] = potential_node_value
							predecessor[connecting_node_id] = actual_node_ID
		future_edges = []
		while actual_node_ID != start_node_ID:
			node_before = vertexes[predecessor[actual_node_ID]]
			self.future_edge_ids.insert(0, node_before.edgesIDs[actual_node_ID])
			actual_node_ID = node_before.ID



		#visited_nodes = [start_node]
		#next_edges = []
		#super_duper_way_of_djikstra_edge_IDs = []
		#def get_next_vertex_ID(visited_nodes):
			#next_edges.append(visited_nodes.connections) #iterieren!, Liste ordnen? oder einfach so lassen
			#"return next_edges.connections.getlowestconnection" -->ordnen wäre für "getlowestconnection" besser oder so...
		#while get_next_vertex_ID(visited_node_IDs) != end_node_ID:
		#	visited_node_IDs.append(get_next_vertex_ID(visited_node_IDs))

