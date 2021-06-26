## read squigles from .fast5 format file


def read_fast5(fast5_names):

	import numpy as np
	import h5py

	retval = dict()

	for fast5_name in fast5_names:
		with h5py.File(fast5_name, 'r') as ifs:
			seq_ids = list(ifs.keys())

			for seq_id in seq_ids:
				key = seq_id.lstrip("read_")
				retval[key] = np.array(ifs[seq_id + "/Raw/Signal"])
	
	return retval
