
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
	def djikstra(self, start_node, end_node): #calculates edge_IDs
		pass
		#visited_nodes = [start_node]
		#next_edges = []
		#super_duper_way_of_djikstra_edge_IDs = []
		#def get_next_vertex_ID(visited_nodes):
			#next_edges.append(visited_nodes.connections) #iterieren!, Liste ordnen? oder einfach so lassen
			#"return next_edges.connections.getlowestconnection" -->ordnen wäre für "getlowestconnection" besser oder so...
		#while get_next_vertex_ID(visited_node_IDs) != end_node_ID:
		#	visited_node_IDs.append(get_next_vertex_ID(visited_node_IDs))

