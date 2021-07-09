def dump_fastl(seq_dict, label_dict, output, seed = None):

	import numpy as np
	np.random.seed(seed)
	rng = np.random.default_rng()

	seq_keys = list(seq_dict.keys())
	rng.shuffle(seq_keys)

	with open(output, 'w') as ofs:
		for key in seq_keys:
			ofs.write(">" + key + " label=" + label_dict[key] + "\n")
			ofs.write(seq_dict[key] + "\n")
