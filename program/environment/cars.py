
class Car:
	def __init__(self, ID, start_node_ID, dest_node_ID, edge_IDs=None):
		self.ID = ID
		self.start_node_ID = start_node_ID
		self.end_node_ID = end_node_ID
		self.djikstra()
		#####nicht nötig, wird in Djikstra generiert###########
		if edge_IDs:
			self.actual_edge = edge_IDs[0]
			self.future_edge_IDs = edge_IDs[1:]
		########################################################
	def djikstra(self): #calculates edge_IDs
		pass


