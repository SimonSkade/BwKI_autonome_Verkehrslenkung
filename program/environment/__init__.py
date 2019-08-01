from environment import net, cars, graphical_output
from environment.net import np

MAX_CYCLES = 10_000_000
SHOW_GRAPHICAL_SIMULATION = False
GRAPHICAL_UPDATE_PERIOD = 100
AUTO_GENERATE_RATE = 0.1

cars = {}
number_cars_generated = 0
action_plan = []

def binary_search_action_plan(new_cycle_nr):
	l = 0
	r = len(action_plan) - 1
	while r - l >= 0:
		m = l + (r-l) // 2
		if action_plan[m].cycle_nr == new_cycle_nr:
			return m
		elif new_cycle_nr < action_plan[m].cycle_nr:
			r = m - 1
		else:
			l = m + 1
	return m

class Action:
	def __init__(self, edge_ID, actual_cycle, car_ID):
		self.edge_ID = edge_ID
		self.cycle_nr = net.network.edges[edge_ID].weight + actual_cycle
		self.car_ID = car_ID
		self.future_edge_IDs = cars[self.car_ID].future_edge_IDs

	def perform_action(self, actual_cycle):
		assert self.cycle_nr == actual_cycle
		if cars[self.car_ID].future_edge_IDs:
			net.network.remove_car(self.edge_ID)
			#update die adjazenzmatrix
			net.network.graph_matrix[net.network.edges[self.edge_ID].v1_id, net.network.edges[self.edge_ID].v2_id] = net.network.edges[self.edge_ID].calc_weight()
			self.edge_ID = cars[self.car_ID].future_edge_IDs[0]
			cars[self.car_ID].actual_edge = self.edge_ID
			del cars[self.car_ID].future_edge_IDs[0]
			net.network.add_car(self.edge_ID)
			#update die adjazenzmatrix
			net.network.graph_matrix[net.network.edges[self.edge_ID].v1_id, net.network.edges[self.edge_ID].v2_id] = net.network.edges[self.edge_ID].calc_weight()
			#create a new action
			new_action = Action(self.edge_ID, actual_cycle, self.car_ID)
			index = binary_search_action_plan(new_action.cycle_nr)
			action_plan.insert(index, new_action)

		else:
			net.network.remove_car(self.edge_ID)
			#update die adjazenzmatrix
			net.network.graph_matrix[net.network.edges[self.edge_ID].v1_id, net.network.edges[self.edge_ID].v2_id] = net.network.edges[self.edge_ID].calc_weight()
			del cars[self.car_ID]


def initialize_network(file): #Liest die benötigten Daten aus einer Datei ein und gibt diese weiter zur Netzwerk-Initialisierung
	def read_matrix(array_str):#parst string zu np array
		lines = array_str.split("\n")
		columns = []
		for i, line in enumerate(lines):
			columns.append([])
			for stringnumber in line.split(" "):
				columns[i].append(int(stringnumber))
		return np.array(columns)	

	with open(file, "r") as f:
		data = f.read()
		data = data.split("\n\n")
		positions = read_matrix(data[0])
		data_a = read_matrix(data[1])
		data_b = read_matrix(data[2])
	net.initialize_network(positions, data_a, data_b)

def manual_simulation(input_file, MAX_CYCLES=MAX_CYCLES, SHOW_GRAPHICAL_SIMULATION=SHOW_GRAPHICAL_SIMULATION, GRAPHICAL_UPDATE_PERIOD=GRAPHICAL_UPDATE_PERIOD):
	def extract_data_from_file(input_file):
		pass #hier sollen die Daten von dem File extrahiert werden #TODO
	cycle_numbers, start_node_ids, end_node_ids = extract_data_from_file(input_file) #output muss sortiert sein
	for cycle in range(MAX_CYCLES):
		if cycle_numbers[0] == cycle:
			new_car = cars.Car(number_cars_generated, start_node_ids[0], end_node_ids[0])
			cars[number_cars_generated] = new_car
			#Aktion generieren
			new_action = Action(new_car.actual_edge, cycle, number_cars_generated)
			index = binary_search_action_plan(new_action.cycle_nr)
			action_plan.insert(index, new_action)
			number_cars_generated += 1
			del cycle_numbers[0]
			del start_node_ids[0]
			del end_node_id[0]

		while action_plan[0].cycle_nr == cycle: #ggf vorgesehene Aktionen ausführen
			action_plan[0].perform_action()
			del action_plan[0]

		if cycle % GRAPHICAL_UPDATE_PERIOD == 0:
			if SHOW_GRAPHICAL_SIMULATION:
				pass #hier soll dann die Graphische Ausgabe geupdated werden



def automatic_simulation(MAX_CYCLES=MAX_CYCLES, SHOW_GRAPHICAL_SIMULATION=SHOW_GRAPHICAL_SIMULATION, GRAPHICAL_UPDATE_PERIOD=GRAPHICAL_UPDATE_PERIOD, AUTO_GENERATE_RATE=AUTO_GENERATE_RATE):
	for cycle in range(MAX_CYCLES):
		if np.random.rand() < AUTO_GENERATE_RATE:
			start_node_id, end_node_id = None, None
			while start_node_id == end_node_id:
				start_node_id, end_node_id = np.random.choice([x for x in range(len(net.network.vertexes))], size=2) #möglicherweise später ändern, dass mehrere End_nodes abgefahren werden
			new_car = cars.Car(number_cars_generated, start_node_id, end_node_id)
			cars[number_cars_generated] = new_car
			#Aktion generieren
			new_action = Action(new_car.actual_edge, cycle, number_cars_generated)
			index = binary_search_action_plan(new_action.cycle_nr)
			action_plan.insert(index, new_action)
			number_cars_generated += 1

		while action_plan[0].cycle_nr == cycle: #ggf vorgesehene Aktionen ausführen
			action_plan[0].perform_action(cycle)
			del action_plan[0]

		if cycle % GRAPHICAL_UPDATE_PERIOD == 0:
			if SHOW_GRAPHICAL_SIMULATION:
				pass #hier soll dann die Graphische Ausgabe geupdated werden

def static_network_plot():
	edges = net.network.edges
	vertexes = net.network.vertexes
	all_nodes_x = []
	all_nodes_y = []
	for node in vertexes:
		all_nodes_x.append(node.position[0])
		all_nodes_y.append(node.position[1])
	all_edges_x = []
	all_edges_y = []
	for edge in edges:
		all_edges_x.append(vertexes[edge.v1_id].position[0])
		all_edges_x.append(vertexes[edge.v2_id].position[0])
		all_edges_x.append(None)
		all_edges_y.append(vertexes[edge.v1_id].position[1])
		all_edges_y.append(vertexes[edge.v2_id].position[1])
		all_edges_y.append(None)
	graphical_output.plot_static(all_edges_x, all_edges_y, all_nodes_x, all_nodes_y)

