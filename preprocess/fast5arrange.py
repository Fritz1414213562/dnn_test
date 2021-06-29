

def arrange_fast5(fastl_name, fast5_dirs, sqgl_unit_size, sqgl_incr_size, data_num = None):
	
	from iomanip import read_fast5, read_fastl, filesindirs
	import numpy as np
	import math

	fast5_suffix = ".fast5"
	fast5_names = filesindirs(fast5_dirs, fast5_suffix)

	labels = read_fastl(fastl_name, output_kind = "label")
	print("Sequences and labels from fastl:", len(labels))
	squiggles = read_fast5(fast5_names)
	print("Squiggles from fast5:", len(squiggles))

	keys = list(set(labels.keys()) & set(squiggles.keys()))
	print("Overlapped:", len(keys))

	out_sqgls = list()
	out_labels = list()

	if data_num == None:
		data_num = len(keys)

	for key in keys[:data_num]:
		squiggle_length = len(squiggles[key])
		if squiggle_length < sqgl_unit_size:
			squiggle = np.pad(squiggles[key], [0, sqgl_unit_size - squiggle_length], 'constant')
			out_sqgls.append(squiggle)
			out_labels.append(labels[key])
		else:
			iter_num = math.ceil(int(squiggle_length - sqgl_unit_size) / sqgl_incr_size)
			i_incr = 0
			for i_incr in range(iter_num):
				start_idx = sqgl_incr_size * i_incr
				end_idx = start_idx + sqgl_unit_size
				out_sqgls.append(squiggles[key][start_idx:end_idx])
				out_labels.append(labels[key])
			start_idx = sqgl_incr_size * (i_incr + 1)
			end_idx = squiggle_length
			out_sqgls.append(np.pad(squiggles[key][start_idx:end_idx], [0, int(start_idx + sqgl_unit_size - squiggle_length)], 'constant'))
			out_labels.append(labels[key])	
	out_sqgls = np.array(out_sqgls, dtype = np.float16)
	out_labels = np.array(out_labels, dtype = np.float16)
	
	return out_sqgls, out_labels



def main(fastl_name, fast5_dirs, output, data_num):

	import h5py
	import sys
	import numpy as np

	BPS2SQGLS = 11.445676382031454
	NUCL_FTP_SIZE = 167.47450040135539
	ESTIMATE_NUCL_SQGLS = int(BPS2SQGLS * NUCL_FTP_SIZE)
	SQGL_INCR_SIZE = int(BPS2SQGLS)
	#SQGL_INCR_SIZE = int(5 * BPS2SQGLS)

	squiggles, labels = arrange_fast5(fastl_name, fast5_dirs, ESTIMATE_NUCL_SQGLS, SQGL_INCR_SIZE, data_num)

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
			subgrp.create_dataset("label", data = np.array([labels[i_instance]]))


if __name__ == "__main__":

	import argparse
	import sys

	parser = argparse.ArgumentParser(description = "Preprocess fast5 files and output as hdf5")
	parser.add_argument("--fastl_file", help = "path to fastl file", required = True)
	parser.add_argument("--fast5_dir", help = "path to fast5 directory", nargs = '*', required = True)
	parser.add_argument("--output", help = "path to the output file (recommended: .ds5)", required = True)
	parser.add_argument("--datanum", help = "the data number for use (training, test)", default = None)
	args = parser.parse_args()

	data_num = None
	if args.datanum == None:
		pass
	else:
		data_num = int(args.datanum)

	main(args.fastl_file, args.fast5_dir, args.output, data_num)
