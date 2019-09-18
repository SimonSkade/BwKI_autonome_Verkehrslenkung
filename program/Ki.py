import numpy as np
from environment import net, car
from copy import deepcopy

EPISODES = 10000
BATCHSIZE = 500



class GNN:
	def __init__(self, graph_matrix): #Initiert das Netzwerk #Eingabe als mehrere konstante Matrizen
		self.gnn = deepcopy(graph_matrix)
		self.diffs = []

	#Netzwerk anpassen, wenn ein Auto auf eine Kante kommt
	def change_weight(self, diff, edge_node1_id, edge_node2_id, num=1):
		self.diffs.append(np.abs(diff))
		self.gnn[edge_node1_id, edge_node2_id] += diff
		if len(self.diffs) >= 10000:
			avg_diff = np.mean(self.diffs)
			unscaled_reward = np.abs(diff) - avg_diff  #Es ist gut wenn der Reward negativ ist
			reward = unscaled_reward * 1 #scale anpassen
			self.gnn[edge_node1_id, edge_node2_id] += reward

class KI:
	def __init__(self):
		self.gnn = GNN(net.network.graph_matrix)

	#berechnet den schnellsten Pfad und speichert die zukünftig abgefahrenen Kanten
	def dijkstra(self, start_node_ID, end_node_ID): 
		num_nodes = len(net.network.vertexes)
		actual_node_ID = start_node_ID
		actual_node_value = 0
		predecessor = np.zeros((num_nodes), dtype='int32')
		unvisited = {}
		edge_ids = []
		for node in	range(num_nodes):
			if node != start_node_ID:
				unvisited[node] = float("Inf")
		for i, weight in enumerate(self.gnn.gnn[actual_node_ID]):
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
			for connecting_node_id, weight in enumerate(self.gnn.gnn[actual_node_ID]):
				if weight != 0:
					if connecting_node_id in unvisited:
						potential_node_value = actual_node_value + weight
						if potential_node_value < unvisited[connecting_node_id]:
							unvisited[connecting_node_id] = potential_node_value
							predecessor[connecting_node_id] = actual_node_ID
		while actual_node_ID != start_node_ID:
			node_before = net.network.vertexes[predecessor[actual_node_ID]]
			edge_ids.insert(0, node_before.edgesIDs[actual_node_ID])
			actual_node_ID = node_before.ID
		return edge_ids

