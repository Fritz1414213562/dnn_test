
def make_squiggle_tables_one_label(squiggles, labels, keys, sqgl_unit_size, sqgl_incr_size, padding):

	import numpy as np
	import math

	out_sqgls = list()
	out_labels = list()

	for key in keys:
		squiggle_length = len(squiggles[key])
		if squiggle_length < sqgl_unit_size:
			squiggle = np.pad(squiggles[key], [0, sqgl_unit_size - squiggle_length], 'constant', constant_values = (padding, padding))
			out_sqgls.append(squiggle)
			out_labels.append(float(labels[key][0]))
		else:
			iter_num = math.ceil(int(squiggle_length - sqgl_unit_size) / sqgl_incr_size)
			i_incr = 0
			for i_incr in range(iter_num):
				start_idx = sqgl_incr_size * i_incr
				end_idx = start_idx + sqgl_unit_size
				out_sqgls.append(squiggles[key][start_idx:end_idx])
				out_labels.append(float(labels[key][0]))
			start_idx = sqgl_incr_size * (i_incr + 1)
			end_idx = squiggle_length
			out_sqgls.append(np.pad(squiggles[key][start_idx:end_idx], [0, int(start_idx + sqgl_unit_size - squiggle_length)], 'constant', constant_values = (padding, padding)))
			out_labels.append(float(labels[key][0]))	
	out_sqgls = np.array(out_sqgls, dtype = np.float16)
	out_labels = np.array(out_labels, dtype = np.float16)
	
	return out_sqgls, out_labels



def make_squiggle_tables_two_label(squiggles, labels, keys, sqgl_unit_size, sqgl_incr_size, padding):

	import numpy as np
	import math

	out_sqgls = list()
	out_labels = list()

	direction_label_dict = {"-" : 0., "+" : 1.}

	for key in keys:
		squiggle_length = len(squiggles[key])
		if squiggle_length < sqgl_unit_size:
			squiggle = np.pad(squiggles[key], [0, sqgl_unit_size - squiggle_length], 'constant', constant_values = (padding, padding))
			out_sqgls.append(squiggle)
			out_labels.append([float(labels[key][0]), direction_label_dict[labels[key][1]]])
		else:
			iter_num = math.ceil(int(squiggle_length - sqgl_unit_size) / sqgl_incr_size)
			i_incr = 0
			for i_incr in range(iter_num):
				start_idx = sqgl_incr_size * i_incr
				end_idx = start_idx + sqgl_unit_size
				out_sqgls.append(squiggles[key][start_idx:end_idx])
				out_labels.append([float(labels[key][0]), direction_label_dict[labels[key][1]]])
			start_idx = sqgl_incr_size * (i_incr + 1)
			end_idx = squiggle_length
			out_sqgls.append(np.pad(squiggles[key][start_idx:end_idx], [0, int(start_idx + sqgl_unit_size - squiggle_length)], 'constant', constant_values = (padding, padding)))
			out_labels.append([float(labels[key][0]), direction_label_dict[labels[key][1]]])
	out_sqgls = np.array(out_sqgls, dtype = np.float16)
	out_labels = np.array(out_labels, dtype = np.float16)
	
	return out_sqgls, out_labels



def make_squiggle_tables_random(squiggles, labels, keys, sqgl_unit_size, padding, out_sqgls, out_labels):

	import numpy as np


	for key in keys:
		squiggle_length = len(squiggles[key])
		if squiggle_length < sqgl_unit_size:
			squiggle = np.pad(squiggles[key], [0, sqgl_unit_size - squiggle_length], 'constant', constant_values = (padding, padding))
			out_sqgls.append(squiggle)
			out_labels.append(float(labels[key][0]))
		else:
			start_idx = np.random.randint(0, squiggle_length - sqgl_unit_size + 1)
			end_idx = start_idx + sqgl_unit_size
			out_sqgls.append(squiggles[key][start_idx:end_idx])
			out_labels.append(float(labels[key][0]))
