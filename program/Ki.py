import numpy as np
import environment
from environment import net, car
from copy import deepcopy

EPISODES = 10000
BATCHSIZE = 500
ALPHA = 0.001


class GNN:
	def __init__(self, graph_matrix): #Initiert das Netzwerk #Eingabe als mehrere konstante Matrizen
		self.gnn = deepcopy(graph_matrix)
		for i in range(self.gnn.shape[0]):
                    for j in range(self.gnn.shape[1]):
                        if self.gnn[i,j] != 0:
                            self.gnn[i,j] = 1

	#Netzwerk anpassen, wenn ein Auto auf eine Kante kommt
	def change_weight(self, diff, edge_node1_id, edge_node2_id, num=1, alpha=ALPHA):
		edge_id = net.network.vertexes[edge_node1_id].edgesIDs[edge_node2_id]
		self.gnn[edge_node1_id, edge_node2_id] += diff #wie viel Gewicht wurde verursacht?
		avg_edge_weight = np.mean([x.weight for x in net.network.edges])
		diff_edge = avg_edge_weight - net.network.edges[edge_id].weight
		diff_cars_per_edge = net.network.edges[net.network.vertexes[edge_node1_id].edgesIDs[edge_node2_id]].n_cars - (len(environment.cars)/len(net.network.edges))
		reward = 0.2*diff_cars_per_edge + np.abs(diff) * (1.25*net.network.edges[net.network.vertexes[edge_node1_id].edgesIDs[edge_node2_id]].n_cars) + 0.1*(avg_edge_weight + 0.5*diff_edge) #reward = Gewichtsänderung * Gewicht #guter Reward: negativ
		self.gnn[edge_node1_id, edge_node2_id] = net.network.edges[edge_id].n_cars +1 #(1-alpha) * self.gnn[edge_node1_id, edge_node2_id] + alpha * (net.network.graph_matrix[edge_node1_id, edge_node2_id] + reward)

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

