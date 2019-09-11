import numpy as np
from environment import net

class GNN:
	def __init__(self, graph_matrix): #Initiert das Netzwerk #Eingabe als mehrere konstante Matrizen
		self.gnn = graph_matrix

	#Netzwerk anpassen, wenn ein Auto auf eine Kante kommt
	def change_weight(self, diff, edge_node1_id, edge_node2_id, num=1):
		self.gnn[edge_node1_id, edge_node2_id] += diff

class KI:
	def __init__(self):
		self.gnn = GNN(net.network.graph_matrix)


