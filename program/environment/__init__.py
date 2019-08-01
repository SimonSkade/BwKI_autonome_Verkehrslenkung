from environment import net, cars, graphical_output
from environment.net import np

MAX_CYCLES = 10_000_000
SHOW_GRAPHICAL_SIMULATION = False
GRAPHICAL_UPDATE_PERIOD = 100
AUTO_GENERATE_RATE = 0.1

cars = []
action_plan = []

class Action:
	def __init__(self, edge_ID, actual_cycle, car_ID):
		self.edge_ID = edge_ID
		self.cycle_nr = net.network.edges[edge_ID].weight + actual_cycle
		self.car_ID = car_ID
		self.future_edges = cars[self.car_ID].future_edges

	def perform_action(self, actual_cycle):
		assert self.cycle_nr == actual_cycle
		if cars[self.car_ID].future_edges:
			net.network.remove_car(self.edge_ID)
			#update die adjazenzmatrix
			net.network.graph_matrix[net.network.edges[self.edge_ID].v1_id, net.network.edges[self.edge_ID].v2_id] = net.network.edges[self.edge_ID].calc_weight()
			self.edge_ID = cars[self.car_ID].future_edges[0]
			cars[self.car_ID].actual_edge = self.edge_ID
			del cars[self.car_ID].future_edges[0]
			net.network.add_car(self.edge_ID)
			#update die adjazenzmatrix
			net.network.graph_matrix[net.network.edges[self.edge_ID].v1_id, net.network.edges[self.edge_ID].v2_id] = net.network.edges[self.edge_ID].calc_weight()
			new_action = Action(self.edge_ID, actual_cycle, self.car_ID)
			


		else:
			net.network.remove_car(self.edge_ID)
			#update die adjazenzmatrix
			net.network.graph_matrix[net.network.edges[self.edge_ID].v1_id, net.network.edges[self.edge_ID].v2_id] = net.network.edges[self.edge_ID].calc_weight()






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

def start_simulation(MAX_CYCLES, SHOW_GRAPHICAL_SIMULATION, GRAPHICAL_UPDATE_PERIOD, AUTO_GENERATE_RATE):
	for i in range(MAX_CYCLES):
		while action_plan[0].cycle_nr == i: #ggf vorgesehene Aktionen ausführen
			#Aktionen ausführen
			#ggf neue Aktion generieren
			#ggf neue Aktion in action_plan einsortieren
			#del action_plan[0]
			pass

		if i % GRAPHICAL_UPDATE_PERIOD == 0:
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

