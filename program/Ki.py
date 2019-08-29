import tensorflow as tf

#Hyperparameter
EPOCHS = 100000
ALPHA = 0.1
EPSILON = 0.8
GAMMA = 0.6
ALPHA_REDUCE_RATE = 0.98
EPSILON_REDUCE_RATE = 0.95

class KI:
	def __init__(self):
		pass

	def train(self, alpha=ALPHA, epsilon=EPSILON, gamma=GAMMA, epochs=EPOCHS, alpha_reduce=ALPHA_REDUCE_RATE, epsilon_reduce=EPSILON_REDUCE_RATE):
		for i in range(epochs):
			#Trainingsprozess


			if i % 1000 == 0:
				#Lern- und Zufallsrate anpassen
				ALPHA *= alpha_reduce
				EPSILON *= epsilon_reduce



