#!/home/simon/anaconda3/bin/python


if __name__=='__main__': #kann man das auch noch anders kontrollieren, dass ein Teil nur ausgeführt wird, wenn die Datei von einer spezifischen anderen Datei aufgerufen/importiert wird?
	import environment
	input_file_network = "../manual_example_data/test_Einlesedatei_netzwerk.txt" #muss später noch allgemein fürs repo funktionieren, nicht nur für meinen PC, ist aber nur ein test #später mit sys?
	input_file_cars = "../manual_example_data/test_einlesedatei_autos.txt"
	environment.initialize_network(input_file_network)
	environment.static_network_plot()
	environment.manual_simulation(input_file_cars)
	#environment.automatic_simulation()




