import torch
import torch.nn as nn
#from environment.net import network
#Hyperparameter
EPOCHS = 100000
ALPHA = 0.1
EPSILON = 0.8
GAMMA = 0.6
ALPHA_REDUCE_RATE = 0.98
EPSILON_REDUCE_RATE = 0.95
dtype = torch.float
device = torch.device("cpu")

class KI:
    def __init__(self):
        n_in = 3 #len(network.vertexes)
        e_in = 5 #len(network.egdes)
        n_hidden1 = 2*n_in
        e_hidden1 = 2*e_in
        hidden2 = 2*e_in
        n_out = e_in
        pass
        #model_nodes = nn.Sequential(OrderedDict([("fc1_n", nn.Linear(n_in, n_hidden1)), ("ReLU1_n", nn.ReLU())])) #für nodes
        #model_edges = nn.Sequential(OrderedDict([("fc1_m", nn.Linear(m_in, m_hidden1)), ("ReLU1_m", nn.ReLU())])) #für edges
        #model3 = nn.Sequential(nn.Linear((n_in+m_in), (n_hidden1+m_hidden1), nn.ReLU(), nn.Linear((n_hidden1+m_hidden1), hidden2), nn.ReLU(), nn.Linear(hidden2, n_out), nn.Sigmoid())) #the network

    def train(self,  input_nodes, input_edges, output, alpha=ALPHA, epsilon=EPSILON, gamma=GAMMA, epochs=EPOCHS, alpha_reduce=ALPHA_REDUCE_RATE, epsilon_reduce=EPSILON_REDUCE_RATE):
        for i in range(epochs):
            #Trainingsprozess


            if i % 1000 == 0:
                #Lern- und Zufallsrate anpassen
                ALPHA *= alpha_reduce
                EPSILON *= epsilon_reduce

    def forward(input_nodes, input_edges, epochs=EPOCHS):
        n_in_hid1_weights = torch.randn(n_in, n_hidden1, device=device, dtype=dtype)
        #print("node weights:" , node_weights)
        e_in_hid1_weights = torch.randn(e_in, e_hidden1, device=device, dtype=dtype)
        #print("egde weights:" , egde_weights)
        hid_1_2_weights = torch.randn(n_hidden1 + e_hidden1, hidden2, device=device, dtype=dtype)
        hid2_out_weights = torch.randn(hidden2, n_out)
        for i in range(1):
            hidden1_n = input_nodes.matmul(n_in_hid1_weights)
            #print("hidden1_n: " , hidden1_n)
            hidden1_e = input_edges.matmul(e_in_hid1_weights)
            #print("hidden1_e: " , hidden1_e)
            hidden1_n_relu = hidden1_n.clamp(min=0)
            hidden1_e_relu = hidden1_e.clamp(min=0)
            hidden_1_out = torch.cat((hidden1_n_relu, hidden1_e_relu)) #the outputs of the node and egde nets are now concatenated
            #print(hidden_1_out)
            hidden2_in = hidden_1_out.matmul(hid_1_2_weights)
            #print(hidden2_in)
            hidden2_relu = hidden2_in.clamp(min=0)
            out_in = hidden2_relu.matmul(hid2_out_weights)
            out_out = torch.sigmoid(out_in)
            print(out_out) #return out_out
            

nodes_in = torch.randn(n_in, device=torch.device("cpu"), dtype=torch.float) #create random inputs for testing
#print("nodes in: " , nodes_in)
edges_in = torch.randn(e_in, device=torch.device("cpu"), dtype=torch.float) #each for nodes and edges
#print("edges_in: ", edges_in)
test(nodes_in, edges_in)
