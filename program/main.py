#!/usr/bin/python


if __name__=='__main__': #kann man das auch noch anders kontrollieren, dass ein Teil nur ausgeführt wird, wenn die Datei von einer spezifischen anderen Datei aufgerufen/importiert wird?
	import environment
	from environment.net import vertex, edge, net

	input_file = "/home/simon/Desktop/wettbewerbe/BwKI/BwKI_autonome_Verkehrslenkung/manual_example_data/test-Einlesedatei.txt" #muss später noch allgemein fürs repo funktionieren, nicht nur für meinen PC, ist aber nur ein test #später mit sys?
	environment.initialize_network(input_file)



