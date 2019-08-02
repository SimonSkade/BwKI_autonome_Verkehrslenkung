
class Car:
	def __init__(self, ID, start_node_ID, end_node_IDs, edge_IDs=None):
		self.ID = ID
		self.start_node_ID = start_node_ID
		self.end_node_IDs = end_node_IDs #typically just one node; is a tuple
		self.djikstra()
		#####nicht nötig, wird in Djikstra generiert###########
		if edge_IDs:
			self.actual_edge = edge_IDs[0]
			self.future_edge_IDs = edge_IDs[1:]
		########################################################
	def djikstra(self): #calculates edge_IDs
		pass


