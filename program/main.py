#!/home/simon/anaconda3/bin/python


if __name__=='__main__': #kann man das auch noch anders kontrollieren, dass ein Teil nur ausgeführt wird, wenn die Datei von einer spezifischen anderen Datei aufgerufen/importiert wird?
    import environment

    #manual network input files
    input_file_network = "../manual_example_data/test_Einlesedatei_netzwerk.txt" #muss später noch allgemein fürs repo funktionieren, nicht nur für meinen PC, ist aber nur ein test #später mit sys?
    #input_file_network = "../manual_example_data/test_saved_network.txt"
    #input_file_network = "../manual_example_data/einlesedatei_braess_paradoxon_netzwerk.txt"#Braess Paradoxon
    environment.initialize_network(input_file_network) #Netzwerk einlesen

    #environment.plot_with_networkx() #Netzwerk plotten
    import simulation as sm
    n_nodes = 10
    n_centers = 2
    #sm.generate_network(n_nodes, n_centers)
    sm.create_KI()

    #sm.save_network("../manual_example_data/test_saved_network.txt")
    
    from environment import car, net

    #tests
    # mycar = car.Car(1, 1, [3])
    # possible_edge_ids = [net.network.vertexes[1].edgesIDs[x] for x in net.network.vertexes[1].connections]
    # print(mycar.step(possible_edge_ids[0]))
    
    #simulations
    #sm.realistic_simulation()
    #environment.plot_with_networkx()
    input_file_cars = "../manual_example_data/test_einlesedatei_autos.txt"
    #input_file_cars = "../manual_example_data/einlesedatei_braess_paradoxon_autos.txt"
    sm.manual_simulation_with_ki(input_file_cars) #Autos manuell einlesen    
    #environment.manual_simulation(input_file_cars)
    #environment.automatic_simulation() #automatische Simulierung starten
