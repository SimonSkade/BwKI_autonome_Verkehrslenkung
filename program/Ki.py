import numpy as np
from environment.net import network

class KI:
	def __init__(self):
		self.gnn = network.graph_matrix