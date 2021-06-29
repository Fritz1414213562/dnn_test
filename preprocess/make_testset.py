def read_dataset(filename):
	import h5py
	import numpy as np

	with h5py.File(filename, 'r') as ifs:

		data_shape = tuple(ifs["DataSize/shape"])
		# dataset = np.zeros(data_shape, dtype=np.float16)
		# labels = np.zeros((data_shape[0],), dtype=np.float16)
		dataset = np.zeros(data_shape, dtype=np.float16)
		labels = np.zeros((data_shape[0],), dtype=np.float16)

		max_current = 0

		for idx in range(data_shape[0]):
			if idx % 100000 == 0:
				print(idx, file = sys.stderr)
			key_path = "DataSet/Instance" + str(idx) + "/"
			# dataset[idx, :] = np.array(ifs[key_path + "squiggle"], dtype=np.float16)
			# labels[idx] = np.array(ifs[key_path + "label"], dtype=np.float16)[0]
			squiggle = np.array(ifs[key_path + "squiggle"], dtype=np.float16)
			if (max_current < np.max(squiggle)) and (np.max(squiggle) < 4096):
				max_current = np.max(squiggle)
			dataset[idx, :] = squiggle
			labels[idx] = np.array(ifs[key_path + "label"], dtype=np.float16)[0]

	dataset /= max_current
	
	return dataset, labels

def main(dataset_name, output_name, validate_size):

	import numpy as np
	import h5py

	dataset, labels = read_dataset(dataset_name)
	instance_num = dataset.shape[0]

	rand_indices = np.random.randint(0, instance_num, (validate_size, ))
	validate = dataset[rand_indices, :]
	answer = labels[rand_indices]

	with h5py.File(output_name, 'w') as ofs:
		grp1 = ofs.create_group("DataSize")
		grp1.create_dataset("shape", data = np.array([validate.shape[0], validate.shape[1]]))
		grp1.create_dataset("instance_num", data = np.array([validate.shape[0]]))
		grp1.create_dataset("squiggle_length", data = np.array([validate.shape[1]]))
		grp2 = ofs.create_group("DataSet")
		for i_instance in range(len(validate)):
			subgrp = grp2.create_group("Instance" + str(i_instance))
			subgrp.create_dataset("squiggle", data = validate[i_instance])
			subgrp.create_dataset("label", data = np.array([answer[i_instance]]))


if __name__ == "__main__":

	import argparse

	import sys

	parser = argparse.ArgumentParser(description = "Test Set Making")
	parser.add_argument("--dataset_dir", help = "path to dataset file", required = True)
	parser.add_argument("--output", help = "path to the output file (recommended: .ds5)", required = True)
	parser.add_argument("--datanum", help = "the data number for use (training, test)", default = None, required = True)
	args = parser.parse_args()

	data_num = None
	if args.datanum == None:
		pass
	else:
		data_num = int(args.datanum)

	main(args.dataset_dir, args.output, data_num)
