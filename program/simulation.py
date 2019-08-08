import numpy as np
import matplotlib.pyplot as plt

#In dieser Datei sollen verschiedene Funktionen geschrieben werden, die eine realistische und praktische Simulation ermöglichen

def generate_nodepositions_per_center(n_nodes): #generiert für jedes Zentrum die Positionen für die Knoten, Anzahl vorgegeben, Normalverteilung um Zentrum, Ränder automatisch generiert
	space_size = 1000
	scale_radius = space_size / 20
	node_positions_x = np.zeros(n_nodes, dtype=np.intc) #Arbeitsweise: x- und y-Werte werden getrennt dargestellt
	node_positions_y = np.zeros(n_nodes, dtype=np.intc) #Wenn das Zentrum sehr nah am Rand liegt, kommt es zu Problemen
	center_position_x = np.random.randint(low=0, high=space_size)
	center_position_y = np.random.randint(low=0, high=space_size)
	node_positions = []
	for i in range(n_nodes):
		node_positions_x[i] = np.round(np.random.normal(loc=center_position_x, scale=scale_radius)) #möglicherweise Knoten außerhalb des Koordinatensystems, deswegen Z. 12-15
		if node_positions_x[i] < 0:
			node_positions_x[i] = 0
		elif node_positions_x[i] > space_size:
			node_positions_x[i] = space_size
		node_positions_y[i] = np.round(np.random.normal(loc=center_position_y, scale=scale_radius)) #dasselbe für y-Werte
		if node_positions_y[i] < 0:
			node_positions_y[i] = 0
		elif node_positions_y[i] > space_size:
			node_positions_y[i] = space_size
		node_positions.append((int(node_positions_x[i]), int(node_positions_y[i])))
	fig = plt.figure()
	plt.scatter(node_positions_x, node_positions_y) #aus Interesse plotten
	plt.scatter(center_position_x, center_position_y, color='red')
	plt.show()
	#Ich habe die Rückgabe geändert zu einer Liste von Knoten mit den Koordinaten
	return node_positions #np.column_stack((node_positions_x, node_positions_y)) #gibt zweidimensionales Array zurück, eine Zeile alle x eine für alle y Koordinaten


node_positions = generate_nodepositions_per_center(40) #Testen (dann muss nur simulation.py aufgerufen werden)
#Funktionierte nicht --> bitte besser testen

def calc_dist(P1, P2): #Die Länge im Koordinatensystem #vielleicht nützlich für die automatische Generierung später
	return np.sqrt((P1[0] - P2[0])**2 + (P1[1] - P2[1])**2)

def generate_edges_without_weights(node_coordinates): #Vielleicht weights am Ende der Funktion einfach generieren
	num_nodes = len(node_coordinates)
	distance_matrix = np.zeros((num_nodes, num_nodes))
	for i in range(num_nodes):
		for j in range(num_nodes):
			if i == j:
				pass
			else:
				distance_matrix[i, j] = calc_dist(node_coordinates[i], node_coordinates[j])
	binary_edge_matrix = np.zeros((num_nodes, num_nodes), dtype=np.intc)
	for i, position in enumerate(node_coordinates):
		num_edges = np.random.choice(np.arange(1,6), p=[0.1, 0.1, 0.45, 0.33, 0.02])
		num_existing_edges = np.sum(binary_edge_matrix[i])
		incoming = True #muss nicht stimmen, aber wird am Ende der Schleife korrigiert
		#Wenn die schleife nicht ausgeführt wird, stimmt es auf jeden Fall
		nodes_sorted = np.argsort(distance_matrix[i])
		nodes_sorted = nodes_sorted[1:]
		while num_existing_edges < num_edges or not incoming:
			distance_index = int(np.round(np.random.rand()**3 * (num_nodes-1)))
			second_node = nodes_sorted[distance_index]
			if i != second_node: #Darf nicht die gleiche Kante sein
				binary_edge_matrix[i, second_node] = 1
				num_existing_edges += 1
				is_one_way = np.random.rand()
				if is_one_way < 0.95:
					binary_edge_matrix[second_node, i] = 1
	return binary_edge_matrix


generate_edges_without_weights(node_positions)
