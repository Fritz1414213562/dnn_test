
def read_aligned_seq(fast5_dirs, paf_name):

	from iomanip import read_fast5, filesindirs, read_id_from_paf

	suffix = ".fast5"
	fast5_names = filesindirs(fast5_dirs, suffix)
	fast5_sqgls = read_fast5(fast5_names)
	print("The number of squiggles in fast5:", len(fast5_sqgls))
	keys = ...
	if paf_name != None:
		aligned_id_set = read_id_from_paf(paf_name)
		print("The number of aligned sequence in paf:", len(aligned_id_set))
		keys = list(aligned_id_set & set(fast5_sqgls.keys()))
		print("Overlapped:", len(keys))
	else:
		keys = list(fast5_sqgls.keys())
	squiggles = dict()
	for key in keys:
		squiggles[key] = fast5_sqgls[key]

	return squiggles


def make_input_data(squiggles, sqgl_unit_size, PADDING):

	import numpy as np
	import math

	sqgl_ids = list()
	table = list()

	for key in squiggles.keys():
		squiggle_length = len(squiggles[key])
		if squiggle_length <= sqgl_unit_size:
			squiggle = np.pad(squiggles[key], [0, sqgl_unit_size - squiggle_length], 'constant', constant_values = (PADDING, PADDING))
			sqgl_ids.append(key)
			table.append(squiggle)
		else:
			iter_num = math.ceil(int(squiggle_length - sqgl_unit_size) / sqgl_unit_size)
			start_idx = 0
			end_idx = sqgl_unit_size
			for idx in range(iter_num):
				squiggle = squiggles[key][start_idx:end_idx]
				sqgl_ids.append(key)
				table.append(squiggle)
				start_idx += sqgl_unit_size
				end_idx += sqgl_unit_size
			squiggle = np.pad(squiggles[key][start_idx:], [0, end_idx - squiggle_length], 'constant', constant_values = (PADDING, PADDING))
			sqgl_ids.append(key)
			table.append(squiggle)
	
	table = np.array(table)
	return sqgl_ids, table


def classify_tables(squiggle_ids, squiggle_table, model_name):

	import tensorflow as tf
	from tensorflow import keras
	from util import util_decimal
	import numpy as np

	model = keras.models.load_model(model_name)
	# prediction
	predicted = model.predict(squiggle_table)
	predicted = util_decimal(predicted).astype(int)
	squiggle_keys = list(set(squiggle_ids))

	retval = dict()

	for squiggle_key in squiggle_keys:
		squiggle_indices = [idx for idx, key in enumerate(squiggle_ids) if key == squiggle_key]
		predicted_label_table = predicted[squiggle_indices]
		label = np.max(predicted_label_table)
		retval[squiggle_key] = label
	
	return retval


def main(fast5_dirs, paf_name, model_name, output):

	from util import standard_normalization
	import numpy as np

	BPS2SQGLS = 11.445676382031454
	NUCL_FTP_SIZE = 167.47450040135539
	PADDING = -4096
	INPUTSIZE = int(BPS2SQGLS * NUCL_FTP_SIZE)

	squiggles = read_aligned_seq(fast5_dirs, paf_name)
	squiggle_ids, squiggle_table = make_input_data(squiggles, INPUTSIZE, PADDING)
	standard_normalization(squiggle_table, PADDING)

	## Classification
	predicted_labels = classify_tables(squiggle_ids, squiggle_table, model_name)
		
	datanum = len(predicted_labels)
	label_values = np.array(list(predicted_labels.values()))
	label_kinds = list(set(predicted_labels.values()))
	labeled_nums = list()
	for label_kind in label_kinds:
		labeled_nums.append(np.count_nonzero(label_values == label_kind))
	
	with open(output, 'w') as ofs:
		ofs.write("Total Squiggles: " + str(datanum) + "\n")
		for idx in range(len(label_kinds)):
			ofs.write("The number of label " + str(label_kinds[idx]) + ": " + str(labeled_nums[idx]))
			ofs.write(" : " + str(100 * labeled_nums[idx] / datanum) + " %\n")


if __name__ == "__main__":

	import argparse

	parser = argparse.ArgumentParser(description = "Classfication")
	parser.add_argument("--fast5_path", help = "path to fast5 file", required = True)
	parser.add_argument("--model_path", help = "path to the model file", required = True)
	parser.add_argument("--output", help = "path to the output file", required = True)
	parser.add_argument("--paf_name", help = "path to alignment file, paf")
	args = parser.parse_args()

	main(args.fast5_path, args.paf_name, args.model_path, args.output)
