import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

#In dieser Datei sollen verschiedene Funktionen geschrieben werden, die eine realistische und praktische Simulation ermöglichen

#Mehrere Zentren wären gut
def generate_nodepositions_per_center(n_nodes, space_size): #generiert für jedes Zentrum die Positionen für die Knoten, Anzahl vorgegeben, Normalverteilung um Zentrum, Ränder automatisch generiert
	space_size = space_size
	scale_radius = space_size / 10
	node_positions = []
	node_positions_x = np.zeros(n_nodes, dtype=np.intc) #Arbeitsweise: x- und y-Werte werden getrennt dargestellt
	node_positions_y = np.zeros(n_nodes, dtype=np.intc) #Wenn das Zentrum sehr nah am Rand liegt, kommt es zu Problemen
	center_position_x = np.random.randint(low=1.5*scale_radius, high=space_size-1.5*scale_radius)
	center_position_y = np.random.randint(low=1.5*scale_radius, high=space_size-1.5*scale_radius)
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
	#plt.scatter(node_positions_x, node_positions_y) #aus Interesse plotten
	#plt.scatter(center_position_x, center_position_y, color='red')
	#Ich habe die Rückgabe geändert zu einer Liste von Knoten mit den Koordinaten
	return node_positions

def generate_random_nodes(n_nodes, space_size):
	scale_radius = space_size / 10
	node_positions_x = []
	node_positions_y = []
	random_nodes = []
	for i in range(n_nodes):
		node_positions_x.append(np.random.randint(low=scale_radius, high=space_size-scale_radius))
		node_positions_y.append(np.random.randint(low=scale_radius, high=space_size-scale_radius))
		random_nodes.append((node_positions_x[i], node_positions_y[i]))
	#plt.scatter(node_positions_x, node_positions_y)
	return random_nodes

def generate_border_nodes(n_border_nodes, space_size):
	space_size = space_size
	node_positions = []
	node_positions_x = np.random.randint(low=0, high=1, size=n_border_nodes) 
	node_positions_y = np.random.randint(low=0, high=1, size=n_border_nodes) 
	for i in range(n_border_nodes):
		if node_positions_x[i] == 1:
			node_positions_x[i] = np.random.choice(2, 1)*space_size
			node_positions_y[i] = np.random.randint(low=0, high=space_size)
		else:
			node_positions_y[i] = np.random.choice(2, 1)*space_size
			node_positions_x[i] = np.random.randint(low=0, high=space_size)
		node_positions.append((int(node_positions_x[i]), int(node_positions_y[i])))
	#plt.scatter(node_positions_x, node_positions_y) #aus Interesse plotten
	return node_positions

def generate_nodes(n_nodes, n_centers=4, space_size=1000):
	n_border_nodes = int(n_nodes * 0.07)
	n_centers = n_centers
	n_nodes_around_centers = int(n_nodes * 0.8)
	n_spread_nodes = int(n_nodes * 0.13)
	space_size = space_size
	node_positions1 = []
	for x in range(n_centers):
		node_positions1 += generate_nodepositions_per_center(abs(int(np.random.normal(loc=n_nodes/n_centers, scale=15))), space_size) #Testen (dann muss nur simulation.py aufgerufen werden)
	node_positions2 = generate_random_nodes(n_spread_nodes, space_size)
	node_positions3 = generate_border_nodes(n_border_nodes, space_size)
	#plt.show()
	node_positions = node_positions1 + node_positions2 + node_positions3
	return node_positions

def plot_edges(node_positions, binary_edge_matrix):
	G = nx.DiGraph()
	for i in range(len(node_positions)):
		for j in range(len(node_positions)):
			if binary_edge_matrix[i, j] == 1:
				G.add_edge(i, j)
	nx.draw(G, pos=node_positions, node_size=8, egde_size= 1)
	plt.show()


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
		nodes_sorted = nodes_sorted[1:] #Die Kante selbst aus dem Knoten löschen
		while num_existing_edges < num_edges or not incoming:
			distance_index = int(np.round(np.random.rand()**3 * (num_nodes-2)))
			second_node = nodes_sorted[distance_index]
			binary_edge_matrix[i, second_node] = 1
			num_existing_edges += 1
			is_one_way = np.random.rand()
			if is_one_way < 0.95:
				binary_edge_matrix[second_node, i] = 1
			incoming = False if np.sum(binary_edge_matrix[:, i]) == 0 else True
	return binary_edge_matrix, distance_matrix

def generate_weights_of_edges(binary_edge_matrix, distance_matrix):
	a_matrix, b_matrix, c_matrix, d_matrix = np.zeros(binary_edge_matrix.shape), np.zeros(binary_edge_matrix.shape), np.zeros(binary_edge_matrix.shape), np.zeros(binary_edge_matrix.shape)
	k = 30
	g = 1
	f = 30
	h = 10
	l = 0.15
	for i in range(binary_edge_matrix.shape[0]):
		for j in range(binary_edge_matrix.shape[0]):
			if binary_edge_matrix[i, j] == 1:
				a_matrix[i, j] = abs(np.random.normal(loc=h, scale=h/5)) * distance_matrix[i, j]
				b_matrix[i, j] = abs(np.random.normal(loc=l, scale=l/5)) * distance_matrix[i, j]
				c_matrix[i, j] = abs(np.random.normal(loc=f, scale=f/5)) * 1/(distance_matrix[i, j] + 1/3)
				d_matrix[i, j] = np.sqrt(abs(np.random.normal(loc=k, scale=k/5)) * distance_matrix[i, j]) + abs(np.random.normal(loc=g, scale=g/5)) * distance_matrix[i, j]
	return a_matrix, b_matrix, c_matrix, d_matrix


node_positions = generate_nodes(100, 2)
binary_edge_matrix, distance_matrix = generate_edges_without_weights(node_positions)
#plot_edges(node_positions, binary_edge_matrix)
a_matrix, b_matrix, c_matrix, d_matrix = generate_weights_of_edges(binary_edge_matrix, distance_matrix)
