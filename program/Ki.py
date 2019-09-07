import torch
import torch.nn as nn
from environment.net import network

EPOCHS = 100
ALPHA = 0.1
EPSILON = 0.8
GAMMA = 0.6
ALPHA_REDUCE_RATE = 0.98
EPSILON_REDUCE_RATE = 0.95
dtype = torch.float
device = torch.device("cpu")

class KI():
    def __init__(self, n_in, e_in):
        #the params
        self.n_in = n_in 
        self.e_in = e_in 
        n_hidden1 = 2*n_in
        e_hidden1 = 2*e_in
        hidden2 = 2*e_in
        n_out = e_in
        
        #the models
        self.model_n = nn.Sequential(nn.Linear(n_in, n_hidden1), nn.ReLU()) #für nodes
        self.model_e = nn.Sequential(nn.Linear(e_in, e_hidden1), nn.ReLU()) #für edges
        self.model2 = nn.Sequential(nn.Linear(n_hidden1+e_hidden1, hidden2), nn.ReLU(), nn.Linear(hidden2, n_out), nn.Sigmoid()) #für die zweite Hälfte
        
    def train(self, net_input, true_output, model, alpha=ALPHA, epsilon=EPSILON, gamma=GAMMA): #one train step
        optimizer = torch.optim.Adam(model.parameters(), alpha) #the first magic line(optimizer)!
        criterion = torch.nn.MSELoss() #the second magic line(loss)! ich benutze hier einen mean squared loss (siehe pytorch doc)
    
        #Trainingsprozess
        #die KI berechnet ihren Output/forward
        pred_output = model(net_input)
        #Wir berechnen den Loss (deine Zeile, Lukas, ich hab hier den Standart-Loss berechnet, den die im Internet verwenden)
        loss = criterion(pred_output, true_output) #hier ist der output gegeben, ich weiß nicht, ob das anwendbar bei uns ist, aber ich bin da ja nicht der Experte
        print(' loss: ', loss.item())
        #Adam kommt zum Einsatz
        optimizer.zero_grad()
        loss.backward()
        #update die parameter
        optimizer.step()
        return model
                
    def forward(self, input_n, input_e, model_n, model_e, model2):
        n_output = model_n(input_n)
        e_output = model_e(input_e)
        n_e_output = torch.cat((n_output, e_output), 0) #the output of the two nets are concatenated to one input for the other net
        output = model2(n_e_output)
        return output
        
        
        
ki = KI(len(network.vertexes), len(network.egdes))       
n_in = torch.randn(ki.n_in)
e_in = torch.randn(ki.e_in)
model2_in = torch.randn(ki.n_in*2+ki.e_in*2)
true_out = torch.randn(ki.e_in)
#print(ki.forward(n_in, e_in, ki.model_n, ki.model_e, ki.model2))
for i in range(EPOCHS):
    ki.model2 = ki.train(model2_in, true_out, ki.model2)

    if i % 1000 == 0:
        #Lern- und Zufallsrate anpassen
        ALPHA *= ALPHA_REDUCE_RATE
        EPSILON *= EPSILON_REDUCE_RATE