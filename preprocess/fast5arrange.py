

def arrange_fast5(fastl_name, fast5_dirs, sqgl_unit_size, sqgl_incr_size, data_num, seed, padding, is_directed_label = False):
	
	from iomanip import read_fast5, read_fastl, filesindirs
	import datasetmake
	import numpy as np
	import math

	fast5_suffix = ".fast5"
	fast5_names = filesindirs(fast5_dirs, fast5_suffix)

	labels = read_fastl(fastl_name, output_kind = "label")
	print("Sequences and labels from fastl:", len(labels))
	squiggles = read_fast5(fast5_names)
	print("Squiggles from fast5:", len(squiggles))

	keys = list(set(labels.keys()) & set(squiggles.keys()))
	label0_keys = np.array([key for key in keys if labels[key][0] == "0"])
	label1_keys = np.array([key for key in keys if labels[key][0] == "1"])
	print("Overlapped:", len(keys))

	np.random.seed(seed)
	rng = np.random.default_rng()

	print("The number of data labeled '0'", len(label0_keys))
	print("The number of data labeled '1'", len(label1_keys))
	label_data_num = min(len(label0_keys), len(label1_keys))
	keys = ...
	if len(label0_keys) < len(label1_keys):
		chosen_label1_keys = rng.choice(label1_keys, size = label_data_num, replace = False)
		keys = np.concatenate([label0_keys, chosen_label1_keys])
	elif len(label0_keys) > len(label1_keys):
		chosen_label0_keys = rng.choice(label0_keys, size = label_data_num, replace = False)
		keys = np.concatenate([chosen_label0_keys, label1_keys])
	else:
		keys = np.concatenate([label0_keys, label1_keys])
	
	rng.shuffle(keys)

	out_sqgls = list()
	out_labels = list()
	datasetmake.make_squiggle_tables_random(squiggles, labels, keys, sqgl_unit_size, padding, out_sqgls, out_labels)

	out_sqgls = np.array(out_sqgls, dtype=np.float16)
	out_labels = np.array(out_labels, dtype=np.float16)

	return out_sqgls, out_labels

#	if data_num == None:
#		data_num = len(keys)
#
#	np.random.seed(seed)
#	rng = np.random.default_rng()
#	random_keys0 = np.random.choice(label0_keys, size = data_num, replace = False)
#	random_keys1 = np.random.choice(label1_keys, size = data_num, replace = False)
#	random_keys = np.concatenate([random_keys0, random_keys1])
#	rng.shuffle(random_keys)
	
#	if is_directed_label:
#		return make_squiggle_tables_two_label(squiggles, labels, random_keys, sqgl_unit_size, sqgl_incr_size, padding)
#	else:
#		return make_squiggle_tables_one_label(squiggles, labels, random_keys, sqgl_unit_size, sqgl_incr_size, padding)
#


def main(fastl_name, fast5_dirs, output, data_num, seed, is_directed_label, make_testset):

	import h5py
	import sys
	import numpy as np
	from util import standard_normalization

	BPS2SQGLS = 11.445676382031454
	NUCL_FTP_SIZE = 167.47450040135539
	ESTIMATE_NUCL_SQGLS = int(BPS2SQGLS * NUCL_FTP_SIZE)
	SQGL_INCR_SIZE = int(BPS2SQGLS)
	TEST_RATE = 0.1
	#SQGL_INCR_SIZE = int(5 * BPS2SQGLS)
	padding = -4096

	squiggles, labels = arrange_fast5(fastl_name, fast5_dirs, ESTIMATE_NUCL_SQGLS, SQGL_INCR_SIZE, data_num, seed, padding, is_directed_label)
#	median_normalization(squiggles, padding)
#	print(labels.shape)
#	label_0_num = np.sum(labels == 0)
#	print("The number of label '0'", label_0_num)
#	label_1_num = np.sum(labels == 1)
#	print("The number off label '1'", label_1_num)
	test_squiggles = ...
	test_labels = ...
	if make_testset:
		rng = np.random.default_rng()
		test_num = int(len(squiggles) * TEST_RATE)
		test_indices = rng.choice(len(squiggles), size = test_num, replace = False)
		data_indices = np.ones(len(squiggles), dtype=bool)
		data_indices[test_indices] = False

		test_squiggles = squiggles[test_indices]
		test_labels = labels[test_indices]
		squiggles = squiggles[data_indices]
		labels = labels[data_indices]

	print("Normalization of Data set")
	standard_normalization(squiggles, padding)
	print("Normalization of Test set")
	standard_normalization(test_squiggles, padding)


	if len(squiggles) != len(labels):
		print("Something wrong !", file = sys.stderr)
		sys.exit()

	with h5py.File(output, 'w') as ofs:
		grp1 = ofs.create_group("DataSize")
		grp1.create_dataset("shape", data = np.array([squiggles.shape[0], squiggles.shape[1]]))
		grp1.create_dataset("instance_num", data = np.array([squiggles.shape[0]]))
		grp1.create_dataset("squiggle_length", data = np.array([squiggles.shape[1]]))
		grp2 = ofs.create_group("DataSet")
		for i_instance in range(len(squiggles)):
			subgrp = grp2.create_group("Instance" + str(i_instance))
			subgrp.create_dataset("squiggle", data = squiggles[i_instance])
			if isinstance(labels[i_instance], np.float16):
				subgrp.create_dataset("label", data = np.array([labels[i_instance]]))
			elif isinstance(labels[i_instance], np.ndarray):
				subgrp.create_dataset("label", data = labels[i_instance])
			else:
				print("The label format is strange!", file = sys.stderr)
				sys.exit()

	if make_testset:
		with h5py.File(output + ".testset.ds5", 'w') as ofs:
			grp1 = ofs.create_group("DataSize")
			grp1.create_dataset("shape", data = np.array([test_squiggles.shape[0], test_squiggles.shape[1]]))
			grp1.create_dataset("instance_num", data = np.array([test_squiggles.shape[0]]))
			grp1.create_dataset("squiggle_length", data = np.array([test_squiggles.shape[1]]))
			grp2 = ofs.create_group("DataSet")
			for i_instance in range(len(test_squiggles)):
				subgrp = grp2.create_group("Instance" + str(i_instance))
				subgrp.create_dataset("squiggle", data = test_squiggles[i_instance])
				if isinstance(test_labels[i_instance], np.float16):
					subgrp.create_dataset("label", data = np.array([test_labels[i_instance]]))
				elif isinstance(test_labels[i_instance], np.ndarray):
					subgrp.create_dataset("label", data = test_labels[i_instance])
				else:
					print("The label format is strange!", file = sys.stderr)
					sys.exit()


if __name__ == "__main__":

	import argparse
	import sys

	parser = argparse.ArgumentParser(description = "Preprocess fast5 files and output as hdf5")
	parser.add_argument("--fastl_file", help = "path to fastl file", required = True)
	parser.add_argument("--fast5_dir", help = "path to fast5 directory", nargs = '*', required = True)
	parser.add_argument("--output", help = "path to the output file (recommended: .ds5)", required = True)
	parser.add_argument("--testset", action = "store_true")
	parser.add_argument("--datanum", help = "the data number for use (training, test)", default = None)
	parser.add_argument("--direct", action = "store_true")
	parser.add_argument("--seed", help = "seed number for random choice")
	args = parser.parse_args()

	data_num = None
	seed_num = 0
	if args.datanum == None:
		pass
	else:
		data_num = int(args.datanum)
	
	if args.seed == None:
		pass
	else:
		seed_num = int(args.seed)

	main(args.fastl_file, args.fast5_dir, args.output, data_num, seed_num, args.direct, args.testset)
