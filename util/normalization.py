

def median_normalization(dataset, padding):

	import numpy as np

	signal_shift = np.median(dataset[dataset != padding])
	print("Median shift:", signal_shift)
	dataset[dataset != padding] -= signal_shift
	signal_scale = np.median(np.abs(dataset[dataset != padding]))
	print("MAD scale:", signal_scale)
	dataset[dataset != padding] /= signal_scale


def standard_normalization(dataset, padding):

	import numpy as np

	signal_shift = np.mean(dataset[dataset != padding])
	print("Mean shift:", signal_shift)
	dataset[dataset != padding] -= signal_shift
	signal_scale = np.std(dataset[dataset != padding], dtype = np.float32)
	print("Std scale:", signal_scale)
	dataset[dataset != padding] /= signal_scale


