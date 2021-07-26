import numpy as np

def read_log(input_log):

	observed = list()
	predicted = list()

	with open(input_log, 'r') as ifs:
		ifs.readline()
		for line in ifs:
			words = line.split()
			predicted.append(int(float(words[0])))
			observed.append(int(float(words[1])))
	
	return np.array(observed), np.array(predicted)


def calculate_accuracy(tf_mat):
	return (tf_mat[0, 0] + tf_mat[1, 1]) / np.sum(tf_mat)


def calculate_sensitivity(tf_mat, label):
	import sys

	if label != 0 and label != 1:
		print("Label should be 0 or 1", file=sys.stderr)
		sys.exit()

	nega_label = 0 if bool(label) else 1

	return tf_mat[label, label] / (tf_mat[label, label] + tf_mat[label, nega_label])


def calculate_precision(tf_mat, label):
	import sys
	if label != 0 and label != 1:
		print("Label should be 0 or 1", file=sys.stderr)
		sys.exit()
	
	nega_label = 0 if bool(label) else 1

	return tf_mat[label, label] / (tf_mat[label, label] + tf_mat[nega_label, label])


def main(input_log, output):

	observed, predicted = read_log(input_log)
	datanum = len(observed)
	true_false_mat = np.zeros((2, 2))

	for idx in range(datanum):
		true_false_mat[observed[idx], predicted[idx]] += 1
	
	with open(output, 'w') as ofs:
		ofs.write("[Label Frequency]\n")
		ofs.write("{0:*>10s} PREDICTED_0 PREDICTED_1\n".format(""))
		ofs.write("OBSERVED_0 {0:11d} {1:11d}\n".format(int(true_false_mat[0, 0]), int(true_false_mat[0, 1])))
		ofs.write("OBSERVED_1 {0:11d} {1:11d}\n".format(int(true_false_mat[1, 0]), int(true_false_mat[1, 1])))

		true_false_mat /= np.sum(true_false_mat)
		ofs.write("\n[Label Probability]\n")
		ofs.write("{0:*>10s} PREDICTED_0 PREDICTED_1\n".format(""))
		ofs.write("OBSERVED_0 {0:11f} {1:11f}\n".format(true_false_mat[0, 0], true_false_mat[0, 1]))
		ofs.write("OBSERVED_1 {0:11f} {1:11f}\n".format(true_false_mat[1, 0], true_false_mat[1, 1]))

		accuracy = calculate_accuracy(true_false_mat)
		ofs.write("\n[Prediction Accuracy]\n")
		ofs.write("accuracy: {0:10f}\n".format(accuracy))

		sensitivity_0 = calculate_sensitivity(true_false_mat, 0)
		sensitivity_1 = calculate_sensitivity(true_false_mat, 1)
		ofs.write("\n[Prediction Sensitivity]\n")
		ofs.write("label_0: {0:10f}\n".format(sensitivity_0))
		ofs.write("label_1: {0:10f}\n".format(sensitivity_1))

		precision_0 = calculate_precision(true_false_mat, 0)
		precision_1 = calculate_precision(true_false_mat, 1)
		ofs.write("\n[Prediction Precision\n")
		ofs.write("label_0: {0:10f}\n".format(precision_0))
		ofs.write("label_1: {0:10f}\n".format(precision_1))




if __name__ == "__main__":

	import argparse

	parser = argparse.ArgumentParser(description = "Validation routine of a nn model")
	parser.add_argument("--predict_log", help = "path to log file of prediction", required = True)
	parser.add_argument("--output", help = "path to output file", required = True)
	args = parser.parse_args()

	main(args.predict_log, args.output)
