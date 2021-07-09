

def read_dataset(filename, density = False):
	import h5py
	import numpy as np
	import sys

	dataset = ...
	labels = ...
	max_current = ...

	with h5py.File(filename, 'r') as ifs:

		data_shape = tuple(ifs["DataSize/shape"])
		dataset = np.zeros(data_shape, dtype=np.float16)
		labels = np.zeros((data_shape[0],), dtype=np.float16)
		max_current = 0

		for idx in range(data_shape[0]):
			if idx % 100000 == 0:
				print(idx, file = sys.stderr)
			key_path = "DataSet/Instance" + str(idx) + "/"
			squiggle = np.array(ifs[key_path + "squiggle"], dtype=np.float16)
			if (max_current < np.max(squiggle)) and (np.max(squiggle) < 4096):
				max_current = np.max(squiggle)
			dataset[idx, :] = squiggle
			labels[idx] = np.array(ifs[key_path + "label"], dtype=np.float16)[0]
	
	if density:
		dataset /= max_current
	else:
		pass
	
	return dataset, labels


def read_one_label_dataset(filename, density = False):
	import h5py
	import numpy as np
	import sys

	dataset = ...
	labels = ...
	max_current = ...

	with h5py.File(filename, 'r') as ifs:

		data_shape = tuple(ifs["DataSize/shape"])
		dataset = np.zeros(data_shape, dtype=np.float16)
		labels = np.zeros((data_shape[0],), dtype=np.float16)
		max_current = 0

		for idx in range(data_shape[0]):
			if idx % 100000 == 0:
				print(idx, file = sys.stderr)
			key_path = "DataSet/Instance" + str(idx) + "/"
			squiggle = np.array(ifs[key_path + "squiggle"], dtype=np.float16)
			if (max_current < np.max(squiggle)) and (np.max(squiggle) < 4096):
				max_current = np.max(squiggle)
			dataset[idx, :] = squiggle
			labels[idx] = np.array(ifs[key_path + "label"], dtype=np.float16)[0]
	
	if density:
		dataset /= max_current
	else:
		pass
	
	return dataset, labels



def read_two_label_dataset(filename, density = False):
	import h5py
	import numpy as np
	import sys

	dataset = ...
	labels = ...
	max_current = ...

	with h5py.File(filename, 'r') as ifs:

		data_shape = tuple(ifs["DataSize/shape"])
		dataset = np.zeros(data_shape, dtype=np.float16)
		labels = np.zeros((data_shape[0], 2), dtype=np.float16)
		max_current = 0

		for idx in range(data_shape[0]):
			if idx % 100000 == 0:
				print(idx, file = sys.stderr)
			key_path = "DataSet/Instance" + str(idx) + "/"
			squiggle = np.array(ifs[key_path + "squiggle"], dtype=np.float16)
			if (max_current < np.max(squiggle)) and (np.max(squiggle) < 4096):
				max_current = np.max(squiggle)
			dataset[idx, :] = squiggle
			labels[idx, :] = np.array(ifs[key_path + "label"], dtype=np.float16)
	
	if density:
		dataset /= max_current
	else:
		pass
	
	return dataset, labels
