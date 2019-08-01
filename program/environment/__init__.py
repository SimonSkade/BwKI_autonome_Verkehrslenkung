from environment import net, cars
from environment.net import np

def initialize_network(file):
	def read_matrix(array_str):
		lines = array_str.split("\n")
		columns = []
		for line in lines:
			for stringnumber in line.split(" "):
				columns.append(int(stringnumber))
		return np.array(columns)	

	with open(file, "r") as f:
		data = f.read()
		data = data.split("\n\n")
		positions = read_matrix(data[0])
		data_a = read_matrix(data[1])
		data_b = read_matrix(data[2])
		