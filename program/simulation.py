import numpy as np

#In dieser Datei sollen verschiedene Funktionen geschrieben werden, die eine realistische und praktische Simulation ermöglichen

def generate_nodepositions_per_center(n_nodes): #generiert für jedes Zentrum die Positionen für die Knoten, Anzahl vorgegeben, Normalverteilung um Zentrum, Ränder automatisch generiert
	node_positions_x = np.zeros(n_nodes) #Arbeitsweise: x- und y-Werte werden getrennt dargestellt
	node_positions_y = np.zeros(n_nodes)
	center_position_x = np.random.randint(low=0, high=50)
	center_position_y = np.random.randint(low=0, high=50)
	for i in range(n_nodes):
		node_positions_x[i] = np.round(np.rand.normal(loc=center_position_x, scale=5)) #möglicherweise Knoten außerhalb des Koordinatensystems, deswegen Z. 12-15
		if node_positions_x[i] < 0:
			node_positions_x[i] = 0
		elif node_positions_x[i] > 50:
			node_positions_x[i] = 50
		node_positions_y[i] = np.round(np.rand.normal(loc=center_position_y, scale=5)) #dasselbe für y-Werte
		if node_positions_y[i] < 0:
			node_positions_y[i] = 0
		elif node_positions_y[i] > 50:
			node_positions_y[i] = 50
	return np.column_stack((node_positions_x, node_positions_y)) #gibt zweidimensionales Array zurück, eine Zeile für eine Position eines Knotens



