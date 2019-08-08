import numpy as np

#In dieser Datei sollen verschiedene Funktionen geschrieben werden, die eine realistische und praktische Simulation ermöglichen

def generate_nodepositions_per_center(n_nodes): #generiert für jedes Zentrum die Positionen für die Knoten, Anzahl vorgegeben, Normalverteilung um Zentrum
	node_positions_x = np.zeros(n_nodes) 
	node_positions_y = np.zeros(n_nodes)
	center_position_x = np.random.randint(low=0, high=50)
	center_position_y = np.random.randint(low=0, high=50)
	for i in range(n_nodes):
		node_positions_x[i] = np.rand.normal(loc=center_position_x, scale=5)
		node_positions_y[i] = np.rand.normal(loc=center_position_y, scale=5)

