import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from environment import net, cars
import Ki
import environment as env
from environment import car

#In dieser Datei sollen verschiedene Funktionen geschrieben werden, die eine realistische und praktische Simulation ermöglichen

class Action:#Stellt einen Kantenwechsel eines Autos zu einer bestimmten Zeit dar
	def __init__(self, actual_cycle, car_ID):
		self.car_ID = car_ID
		self.edge_ID = cars[car_ID].actual_edge
		self.cycle_nr = round(net.network.edges[self.edge_ID].weight + actual_cycle)

	def perform_action(self, actual_cycle): #führt die Aktion aus
		#assert self.cycle_nr == actual_cycle
		edge1_node1_ID = net.network.edges[self.edge_ID].v1_id
		edge1_node2_ID = net.network.edges[self.edge_ID].v2_id
		if cars[self.car_ID].future_edge_IDs:
			diff = net.network.remove_car(self.edge_ID)
			gnn.change_weight(diff, edge1_node1_ID, edge1_node2_ID) #nicht aufgerufen!!!
			self.edge_ID = cars[self.car_ID].future_edge_IDs[0]
			cars[self.car_ID].actual_edge = self.edge_ID
			del cars[self.car_ID].future_edge_IDs[0]
			diff = net.network.add_car(self.edge_ID)
			edge2_node1_ID = net.network.edges[self.edge_ID].v1_id
			edge2_node2_ID = net.network.edges[self.edge_ID].v2_id
			gnn.change_weight(diff, edge2_node1_ID, edge2_node2_ID)
			#Erstelle eine neue Aktion für den nächsten Kantenwechsel
			new_action = Action(actual_cycle, self.car_ID)
			index = env.linear_search_action_plan(new_action.cycle_nr)
			env.action_plan.insert(index, new_action)

		else:#Das Auto hat sein Ziel erreicht
			diff = net.network.remove_car(self.edge_ID)
			gnn.change_weight(diff, edge1_node1_ID, edge1_node2_ID)
			del cars[self.car_ID] #Lösche das Auto




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
	global n_border_nodes
	n_border_nodes = int(n_nodes * 0.07)
	n_centers = n_centers
	n_nodes_around_centers = int(n_nodes * 0.8)
	n_spread_nodes = int(n_nodes * 0.13)
	space_size = space_size
	node_positions1 = []
	for x in range(n_centers):
		node_positions1 += generate_nodepositions_per_center(int(n_nodes_around_centers/n_centers), space_size) #Testen (dann muss nur simulation.py aufgerufen werden)
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
	global distance_matrix
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
		num_edges = np.random.choice(np.arange(1,6), p=[0.1, 0.3, 0.4, 0.2, 0])
		num_existing_edges = np.sum(binary_edge_matrix[i])
		incoming = True #muss nicht stimmen, aber wird am Ende der Schleife korrigiert
		#Wenn die schleife nicht ausgeführt wird, stimmt es auf jeden Fall
		nodes_sorted = np.argsort(distance_matrix[i])
		nodes_sorted = nodes_sorted[1:] #Die Kante selbst aus dem Knoten löschen
		while num_existing_edges < num_edges or not incoming:
			distance_index = int(np.round(np.random.rand()**10 * (num_nodes-2)))
			second_node = nodes_sorted[distance_index]
			binary_edge_matrix[i, second_node] = 1
			is_one_way = np.random.rand()
			if is_one_way < 0.95:
				binary_edge_matrix[second_node, i] = 1
			incoming = False if np.sum(binary_edge_matrix[:, i]) == 0 else True
			num_existing_edges = np.sum(binary_edge_matrix[i])
	return binary_edge_matrix, distance_matrix

def generate_weights_of_edges(binary_edge_matrix, distance_matrix):
	a_matrix, b_matrix, c_matrix, d_matrix = np.zeros(binary_edge_matrix.shape), np.zeros(binary_edge_matrix.shape), np.zeros(binary_edge_matrix.shape), np.zeros(binary_edge_matrix.shape)
	k = 0.4
	g = 0.025
	f = 10
	h = 0.25
	l = 0.33
	for i in range(binary_edge_matrix.shape[0]):
		for j in range(binary_edge_matrix.shape[0]):
			if binary_edge_matrix[i, j] == 1:
				a_matrix[i, j] = abs(np.random.normal(loc=h, scale=h/10)) * distance_matrix[i, j]
				b_matrix[i, j] = abs(np.random.normal(loc=l, scale=l/5)) * distance_matrix[i, j]
				c_matrix[i, j] = abs(np.random.normal(loc=f, scale=f/10)) * 1/(distance_matrix[i, j] + 1/3)
				d_matrix[i, j] = np.sqrt(abs(np.random.normal(loc=k, scale=k/10)) * distance_matrix[i, j]) + abs(np.random.normal(loc=g, scale=g/10)) * distance_matrix[i, j]
	return a_matrix, b_matrix, c_matrix, d_matrix

def generate_network(n_nodes, n_centers=2):
	global node_positions, a_matrix, b_matrix, c_matrix, d_matrix
	node_positions = generate_nodes(n_nodes, n_centers)
	binary_edge_matrix, distance_matrix = generate_edges_without_weights(node_positions)
	#plot_edges(node_positions, binary_edge_matrix)
	a_matrix, b_matrix, c_matrix, d_matrix = generate_weights_of_edges(binary_edge_matrix, distance_matrix)
	net.initialize_network(node_positions, a_matrix, b_matrix, c_matrix, d_matrix)

def save_network(filename):
	global node_positions, a_matrix, b_matrix, c_matrix, d_matrix
	with open(filename, "w") as file:
		for position in node_positions:
			file.write(str(position[0]) + " " + str(position[1]) + "\n")
		file.write("\n")
		for i in range(len(node_positions)):
			for j in range(len(node_positions)-1):
				file.write(str(a_matrix[i,j]) + " ")
			file.write(str(a_matrix[i,-1]) + "\n")
		file.write("\n")
		for i in range(len(node_positions)):
			for j in range(len(node_positions)-1):
				file.write(str(b_matrix[i,j]) + " ")
			file.write(str(b_matrix[i,-1]) + "\n")
		file.write("\n")
		for i in range(len(node_positions)):
			for j in range(len(node_positions)-1):
				file.write(str(c_matrix[i,j]) + " ")
			file.write(str(c_matrix[i,-1]) + "\n")
		file.write("\n")
		for i in range(len(node_positions)):
			for j in range(len(node_positions)-1):
				file.write(str(d_matrix[i,j]) + " ")
			file.write(str(d_matrix[i,-1]) + "\n")
		file.write("\n")
		file.close()

MAX_CYCLES = 100000
SHOW_GRAPHICAL_SIMULATION = True
UPDATE_PERIOD = 2000
AUTO_GENERATE_RATE = 0.7


#Simuliert Netzwerkströme automatisch
def realistic_simulation(MAX_CYCLES=MAX_CYCLES, SHOW_GRAPHICAL_SIMULATION=SHOW_GRAPHICAL_SIMULATION, UPDATE_PERIOD=UPDATE_PERIOD, AUTO_GENERATE_RATE=AUTO_GENERATE_RATE):
	global n_border_nodes, distance_matrix
	number_cars_generated = 0
	n_nodes = len(env.net.network.vertexes)
	border_nodes_start = n_nodes - n_border_nodes
	border_nodes_end = n_nodes - 1
	higher_probability_factor = 4
	prob_node = 1/(border_nodes_start + higher_probability_factor*n_border_nodes)
	for cycle in range(MAX_CYCLES):
		while np.random.rand() < AUTO_GENERATE_RATE:
			start_node_id, end_node_id = None, None
			start_node_id = np.random.choice([x for x in range(n_nodes)], p=[prob_node for x in range(border_nodes_start)] + [higher_probability_factor * prob_node for x in range(n_border_nodes)])
			is_border_node = np.random.choice([0,1], p=[prob_node*border_nodes_start, higher_probability_factor*prob_node*n_border_nodes])
			if is_border_node == 1:
				distances_to_border_nodes = distance_matrix[start_node_id, border_nodes_start:]
				nodes_sorted = np.argsort(distances_to_border_nodes)
				nodes_sorted = nodes_sorted[1:]
				distance_index = int(np.round((1-np.random.rand()**2) * (len(nodes_sorted) - 1)))
				end_node_id = nodes_sorted[distance_index]
			else:
				distances_to_normal_nodes = distance_matrix[start_node_id, :border_nodes_start]
				nodes_sorted = np.argsort(distances_to_normal_nodes)
				nodes_sorted = nodes_sorted[1:]
				distance_index = int(np.round((1-np.random.rand()**2) * (len(nodes_sorted) - 1)))
				end_node_id = nodes_sorted[distance_index]

			# end_node_id = [np.random.choice([x for x in range(len(net.network.vertexes))])] #später noch mehrere End_nodes ermöglichen
			new_car = car.Car(number_cars_generated, start_node_id, [end_node_id])
			diff = net.network.add_car(new_car.actual_edge)
			edge_node1_ID = net.network.edges[new_car.actual_edge].v1_id
			edge_node2_ID = net.network.edges[new_car.actual_edge].v2_id			
			gnn.change_weight(diff, edge_node1_ID, edge_node2_ID)

			env.cars[number_cars_generated] = new_car
			#Aktion generieren
			new_action = Action(cycle, number_cars_generated)
			index = env.linear_search_action_plan(new_action.cycle_nr)
			env.action_plan.insert(index, new_action)
			number_cars_generated += 1
		try:
			while env.action_plan[0].cycle_nr == cycle: #ggf vorgesehene Aktionen ausführen
				env.action_plan[0].perform_action(cycle)
				del env.action_plan[0]
		except IndexError:
			pass
		if cycle % UPDATE_PERIOD == 0:
			print(f"Now reached cycle {cycle}. Number of cars simulated: {number_cars_generated}")
			flow_rate = np.sum([x.n_cars / x.weight for x in env.net.network.edges])
			avg_flow_rate = flow_rate/len(env.cars)
			#avg_actual_time_per_edge = 1 / flow_rate # sollte proportional zu folgendem sein: np.sum([net.network.edges[x.actual_edge] for x in env.cars])
			avg_total_time_per_edge = np.sum([np.sum([env.net.network.edges[x.future_edge_IDs[y]].weight for y in range(len(x.future_edge_IDs))]) + env.net.network.edges[x.actual_edge].weight for x in env.cars.values()]) / np.sum([len(x.future_edge_IDs) + 1 for x in env.cars.values()])
			avg_total_time_per_car = np.sum([np.sum([env.net.network.edges[x.future_edge_IDs[y]].weight for y in range(len(x.future_edge_IDs))]) + env.net.network.edges[x.actual_edge].weight for x in env.cars.values()]) / len(env.cars)
			print(f"Absolute Flow rate: {flow_rate};\nDurchschnittliche Flow Rate: {avg_flow_rate};\nDurchschnittliche Zeit pro befahrene Kante: {avg_total_time_per_edge};")
			print(f"Durchschnittliche Gesamtfahrzeit pro Auto: {avg_total_time_per_car};\nAnzahl Autos gesamt: {len(env.cars)}")
			print("\n\n")
			if SHOW_GRAPHICAL_SIMULATION:
				env.plot_with_networkx()

	#Simuliert Netzwerkströme automatisch
def realistic_simulation_with_ki(MAX_CYCLES=MAX_CYCLES, SHOW_GRAPHICAL_SIMULATION=SHOW_GRAPHICAL_SIMULATION, UPDATE_PERIOD=UPDATE_PERIOD, AUTO_GENERATE_RATE=AUTO_GENERATE_RATE): 
#TODO: Mehrere End-Nodes möglich machen
	global n_border_nodes, distance_matrix
	number_cars_generated = 0
	n_nodes = len(env.net.network.vertexes)
	border_nodes_start = n_nodes - n_border_nodes
	border_nodes_end = n_nodes - 1
	higher_probability_factor = 4
	prob_node = 1/(border_nodes_start + higher_probability_factor*n_border_nodes)
	for cycle in range(MAX_CYCLES):
		while np.random.rand() < AUTO_GENERATE_RATE:
			start_node_id, end_node_id = None, None
			start_node_id = np.random.choice([x for x in range(n_nodes)], p=[prob_node for x in range(border_nodes_start)] + [higher_probability_factor * prob_node for x in range(n_border_nodes)])
			is_border_node = np.random.choice([0,1], p=[prob_node*border_nodes_start, higher_probability_factor*prob_node*n_border_nodes])
			if is_border_node == 1:
				distances_to_border_nodes = distance_matrix[start_node_id, border_nodes_start:]
				nodes_sorted = np.argsort(distances_to_border_nodes)
				nodes_sorted = nodes_sorted[1:]
				distance_index = int(np.round((1-np.random.rand()**2) * (len(nodes_sorted) - 1)))
				end_node_id = nodes_sorted[distance_index]
			else:
				distances_to_normal_nodes = distance_matrix[start_node_id, :border_nodes_start]
				nodes_sorted = np.argsort(distances_to_normal_nodes)
				nodes_sorted = nodes_sorted[1:]
				distance_index = int(np.round((1-np.random.rand()**2) * (len(nodes_sorted) - 1)))
				end_node_id = nodes_sorted[distance_index]

			# end_node_id = [np.random.choice([x for x in range(len(net.network.vertexes))])] #später noch mehrere End_nodes ermöglichen
			new_car = car.Car(number_cars_generated, start_node_id, [end_node_id], False)
			edge_ids = ki.dijkstra(start_node_id, end_node_id)	
			new_car.set_params(edge_ids)
			diff = net.network.add_car(new_car.actual_edge)
			edge_node1_ID = net.network.edges[new_car.actual_edge].v1_id
			edge_node2_ID = net.network.edges[new_car.actual_edge].v2_id			
			gnn.change_weight(diff, edge_node1_ID, edge_node2_ID)

			env.cars[number_cars_generated] = new_car
			#Aktion generieren
			new_action = Action(cycle, number_cars_generated)
			index = env.linear_search_action_plan(new_action.cycle_nr)
			env.action_plan.insert(index, new_action)
			number_cars_generated += 1
		try:
			while env.action_plan[0].cycle_nr == cycle: #ggf vorgesehene Aktionen ausführen
				env.action_plan[0].perform_action(cycle)
				del env.action_plan[0]
		except IndexError:
			pass
		if cycle % UPDATE_PERIOD == 0:
			print(f"Now reached cycle {cycle}. Number of cars simulated: {number_cars_generated}")
			flow_rate = np.sum([x.n_cars / x.weight for x in env.net.network.edges])
			avg_flow_rate = flow_rate/len(env.cars)
			#avg_actual_time_per_edge = 1 / flow_rate # sollte proportional zu folgendem sein: np.sum([net.network.edges[x.actual_edge] for x in env.cars])
			avg_total_time_per_edge = np.sum([np.sum([env.net.network.edges[x.future_edge_IDs[y]].weight for y in range(len(x.future_edge_IDs))]) + env.net.network.edges[x.actual_edge].weight for x in env.cars.values()]) / np.sum([len(x.future_edge_IDs) + 1 for x in env.cars.values()])
			avg_total_time_per_car = np.sum([np.sum([env.net.network.edges[x.future_edge_IDs[y]].weight for y in range(len(x.future_edge_IDs))]) + env.net.network.edges[x.actual_edge].weight for x in env.cars.values()]) / len(env.cars)
			print(f"Absolute Flow rate: {flow_rate};\nDurchschnittliche Flow Rate: {avg_flow_rate};\nDurchschnittliche Zeit pro befahrene Kante: {avg_total_time_per_edge};")
			print(f"Durchschnittliche Gesamtfahrzeit pro Auto: {avg_total_time_per_car};\nAnzahl Autos gesamt: {len(env.cars)}")
			print("\n\n")
			if SHOW_GRAPHICAL_SIMULATION:
				env.plot_with_networkx()


#Simuliert die Verkehrsströme wie in einem input file vorgegeben
def manual_simulation_with_ki(input_file, MAX_CYCLES=MAX_CYCLES, SHOW_GRAPHICAL_SIMULATION=SHOW_GRAPHICAL_SIMULATION, UPDATE_PERIOD=UPDATE_PERIOD):
	from environment import car
	from environment import net
	def extract_data_from_file(input_file):
		cycle_numbers, start_node_ids, end_node_ids = [], [], []
		with open(input_file, "r") as f:
			data = f.read()
			lines = data.split("\n")
			for line in lines:
				if line == "":
					pass
				else:
					columns = line.split(" ")
					cycle_nr = int(columns[0])
					index = env.linear_search(cycle_numbers, cycle_nr)
					cycle_numbers.insert(index, cycle_nr)
					start_node_ids.insert(index, int(columns[1]))
					end_nodes = columns[2].split(",")
					end_node_ids.insert(index, [int(node) for node in end_nodes])
		return cycle_numbers, start_node_ids, end_node_ids
	number_cars_generated = 0
	cycle_numbers, start_node_ids, end_node_ids = extract_data_from_file(input_file) #output muss sortiert sein
	for cycle in range(MAX_CYCLES):
		try:
			while cycle_numbers[0] == cycle:
				new_car = car.Car(number_cars_generated, start_node_ids[0], end_node_ids[0], False)
				edge_ids = ki.dijkstra(start_node_ids[0], end_node_ids[0])
				new_car.set_params(edge_ids)
				diff = net.network.add_car(new_car.actual_edge)
				edge_node1_ID = net.network.edges[new_car.actual_edge].v1_id
				edge_node2_ID = net.network.edges[new_car.actual_edge].v2_id			
				gnn.change_weight(diff, edge_node1_ID, edge_node2_ID)
				cars[number_cars_generated] = new_car
				#Aktion generieren
				new_action = Action(cycle, number_cars_generated)
				index = env.linear_search_action_plan(new_action.cycle_nr)
				env.action_plan.insert(index, new_action)
				number_cars_generated += 1
				del cycle_numbers[0]
				del start_node_ids[0]
				del end_node_ids[0]
		except IndexError:
			pass
		try:
			while env.action_plan[0].cycle_nr == cycle: #ggf vorgesehene Aktionen ausführen
				env.action_plan[0].perform_action(cycle)
				del env.action_plan[0]
		except IndexError:
			pass
		if cycle % UPDATE_PERIOD == 0:
			print(f"Now reached cycle {cycle}. Number of cars simulated: {number_cars_generated}")
			flow_rate = np.sum([x.n_cars / x.weight for x in net.network.edges])
			avg_flow_rate = flow_rate/len(cars)
			#avg_actual_time_per_edge = 1 / flow_rate # sollte proportional zu folgendem sein: np.sum([net.network.edges[x.actual_edge] for x in cars])
			avg_total_time_per_edge = np.sum([np.sum([net.network.edges[x.future_edge_IDs[y]].weight for y in range(len(x.future_edge_IDs))]) + net.network.edges[x.actual_edge].weight for x in cars.values()]) / np.sum([len(x.future_edge_IDs) + 1 for x in cars.values()])
			avg_total_time_per_car = np.sum([np.sum([net.network.edges[x.future_edge_IDs[y]].weight for y in range(len(x.future_edge_IDs))]) + net.network.edges[x.actual_edge].weight for x in cars.values()]) / len(cars)
			print(f"Absolute Flow rate: {flow_rate};\nDurchschnittliche Flow Rate: {avg_flow_rate};\nDurchschnittliche Zeit pro befahrene Kante: {avg_total_time_per_edge};")
			print(f"Durchschnittliche Gesamtfahrzeit pro Auto: {avg_total_time_per_car};\nAnzahl Autos gesamt: {len(cars)}")

			if SHOW_GRAPHICAL_SIMULATION:
				#env.plot_with_networkx() #hier soll dann die Graphische Ausgabe geupdated werden
				env.plot_with_networkx_num_cars()


def create_KI():
	global ki, gnn
	ki = Ki.KI()
	gnn = ki.gnn

