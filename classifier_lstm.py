import tensorflow as tf
from tensorflow.keras import layers, preprocessing
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Dense, Activation, Masking
from tensorflow.keras.layers import LSTM
import numpy as np
import matplotlib.pyplot as plt
import sys
import math
import subprocess



def read_dataset(filename):
	import h5py
	import numpy as np

	with h5py.File(filename, 'r') as ifs:

		data_shape = tuple(ifs["DataSize/shape"])
		dataset = np.zeros(data_shape, dtype=np.int16)
		labels = np.zeros((data_shape[0],), dtype=np.int8)

		for idx in range(data_shape[0]):
			if idx % 100000 == 0:
				print(idx, file = sys.stderr)
			key_path = "DataSet/Instance" + str(idx) + "/"
			dataset[idx, :] = np.array(ifs[key_path + "squiggle"], dtype=np.int16)
			labels[idx] = np.array(ifs[key_path + "label"], dtype=np.int8)[0]
	
	return dataset, labels


def main():

	tf.random.set_seed(199803132)
	np.random.seed(271828189)

	data = list()

	dataset, labels = read_dataset("dataset.ds5")
	instance_num = dataset.shape[0]
	
	n_hidden = 100
	out_neurons = 1
	batch_size = 1024
	
	model = Sequential()
	model.add(LSTM(n_hidden))
	model.add(Dense(out_neurons))
	model.add(Activation("sigmoid"))
	optimizer = Adam(learning_rate = 0.001)
	model.compile(loss = "mean_squared_error", optimizer = optimizer)
#	print(model.summary())

	#sys.exit()
	early_stopping = EarlyStopping(monitor = "val_loss", mode = "auto", patience = 20)
	#model.fit(small_data, small_target, batch_size = batch_size, epochs = 100, validation_split = 0.1, callbacks = [early_stopping])
	model.fit(dataset, labels, batch_size = batch_size, epochs = 100, validation_split = 0.1, callbacks = [early_stopping])
	model.save("test_model")
	
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
