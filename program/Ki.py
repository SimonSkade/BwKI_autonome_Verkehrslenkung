import torch
import torch.nn as nn
from environment.net import network
#Hyperparameter
EPOCHS = 100000
ALPHA = 0.1
EPSILON = 0.8
GAMMA = 0.6
ALPHA_REDUCE_RATE = 0.98
EPSILON_REDUCE_RATE = 0.95

class KI:
	def __init__(self):
		n_in = len(network.vertexes)
		m_in = len(network.egdes)
		n_hidden1 = 2*n_in
		m_hidden1 = 2*m_in
		hidden2 = 2*m_in
		n_out = m_in
		#model1 = nn.Sequential(OrderedDict([("fc1_n", nn.Linear(n_in, n_hidden1)), ("ReLU1_n", nn.ReLU())])) #für n
		#model2 = nn.Sequential(OrderedDict([("fc1_m", nn.Linear(m_in, m_hidden1)), ("ReLU1_m", nn.ReLU())])) #für m
		model3 = nn.Sequential(nn.Linear((n_in+m_in), (n_hidden1+m_hidden1), nn.ReLU(), nn.Linear((n_hidden1+m_hidden1), hidden2), nn.ReLU(), nn.Linear(hidden2, n_out), nn.Sigmoid()))

	def train(self, alpha=ALPHA, epsilon=EPSILON, gamma=GAMMA, epochs=EPOCHS, alpha_reduce=ALPHA_REDUCE_RATE, epsilon_reduce=EPSILON_REDUCE_RATE):
		for i in range(epochs):
			#Trainingsprozess


			if i % 1000 == 0:
				#Lern- und Zufallsrate anpassen
				ALPHA *= alpha_reduce
				EPSILON *= epsilon_reduce



