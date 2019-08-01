
class Car:
	def __init__(self, start_node_ID, dest_node_ID):
		self.start_node_ID = start_node_ID
		self.dest_node_ID = dest_node_ID

	def djikstra(self):
		pass

	def set_future_edges(self, edges_ID):
		self.actual_edge_ID = egdes_ID[0]
		self.future_edges_ID = edges_ID[1:]

