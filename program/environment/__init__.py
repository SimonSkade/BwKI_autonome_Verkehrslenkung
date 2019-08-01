from environment import net, cars, graphical_output
from environment.net import np

MAX_CYCLES = 10_000_000
SHOW_GRAPHICAL_SIMULATION = False
GRAPHICAL_UPDATE_PERIOD = 100
AUTO_GENERATE_RATE = 0.1

class Action:
	pass


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

		if i % GRAPHICAL_UPDATE_PERIOD == 0:
			if SHOW_GRAPHICAL_SIMULATION:
				pass #hier soll dann die Graphische Ausgabe geupdated werden
