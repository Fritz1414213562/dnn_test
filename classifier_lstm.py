import tensorflow as tf
from tensorflow.keras import layers, preprocessing
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Dense, Activation, Masking
from tensorflow.keras.layers import LSTM
from iomanip import read_dataset
import numpy as np
import matplotlib.pyplot as plt
import sys
import math
import subprocess



def main():

	tf.random.set_seed(199803132)
	np.random.seed(271828189)

	data = list()

	dataset, labels = read_dataset("dataset.ds5", density = True)
	dataset = dataset.reshape(dataset.shape[0], dataset.shape[1], 1)
	labels = labels.reshape(labels.shape[0], 1)
	instance_num = dataset.shape[0]
	
	n_hidden = 100
	in_neurons = 1
	out_neurons = 1
	batch_size = 256
	
	model = Sequential()
	model.add(Masking(mask_value = 0, input_shape = (None, in_neurons)))
	model.add(LSTM(n_hidden))
	model.add(Dense(out_neurons))
	model.add(Activation("sigmoid"))
	optimizer = Adam(learning_rate = 0.001)
	model.compile(loss = "mean_squared_error", optimizer = optimizer)
	# print(model.summary())

	#sys.exit()
	early_stopping = EarlyStopping(monitor = "val_loss", mode = "auto", patience = 20)
	#model.fit(small_data, small_target, batch_size = batch_size, epochs = 100, validation_split = 0.1, callbacks = [early_stopping])
	model.fit(dataset, labels, batch_size = batch_size, epochs = 200, validation_split = 0.1, callbacks = [early_stopping])
	model.save("test_lstm_model")
	
	## using train data
	validate_size = 1000
	rand_indices = np.random.randint(0, instance_num, (validate_size, ))
	validate = dataset[rand_indices, :]
	answer = labels[rand_indices]
	predicted = model.predict(validate)
	print("PREDICTED")
	print(predicted)
	print("ANSWER")
	print(answer)



if __name__ == "__main__":

	main()
