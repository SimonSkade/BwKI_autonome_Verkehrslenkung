#!/home/simon/anaconda3/bin/python


if __name__=='__main__': #kann man das auch noch anders kontrollieren, dass ein Teil nur ausgeführt wird, wenn die Datei von einer spezifischen anderen Datei aufgerufen/importiert wird?
	import environment
	#input_file_network = "../manual_example_data/test_Einlesedatei_netzwerk.txt" #muss später noch allgemein fürs repo funktionieren, nicht nur für meinen PC, ist aber nur ein test #später mit sys?
	#environment.initialize_network(input_file_network) #Netzwerk einlesen
	#environment.static_network_plot() #Netzwerk plotten
	import simulation as sm
	n_nodes = 100
	n_centers = 2
	sm.generate_network(n_nodes, n_centers)
	sm.save_network("../manual_example_data/test_saved_network.txt")
	#Hier können mit sm.function() dann die Simulationen ausgeführt werden
	#environment.plot_with_networkx()
	#input_file_cars = "../manual_example_data/test_einlesedatei_autos.txt"
	#environment.manual_simulation(input_file_cars) #Autos manuell einlesen
	environment.automatic_simulation() #automatische Simulierung starten

	


