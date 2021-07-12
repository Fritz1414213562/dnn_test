import numpy as np

def read_log(input_log):

	observed = list()
	predicted = list()

	with open(input_log, 'r') as ifs:
		ifs.readline()
		for line in ifs:
			words = line.split()
			predicted.append([int(float(words[0])), int(float(words[1]))])
			observed.append([int(float(words[2])), int(float(words[3]))])
	
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


def true_false_class0(total_mat):
	retval = np.zeros((2, 2))
	retval[0, 0] = total_mat[0, 0] + total_mat[0, 1] + total_mat[1, 0] + total_mat[1, 1]
	retval[0, 1] = total_mat[0, 2] + total_mat[0, 3] + total_mat[1, 2] + total_mat[1, 3]
	retval[1, 0] = total_mat[2, 0] + total_mat[2, 1] + total_mat[3, 0] + total_mat[3, 1]
	retval[1, 1] = total_mat[2, 2] + total_mat[2, 3] + total_mat[3, 2] + total_mat[3, 3]
	return retval


def true_false_class1(total_mat):
	retval = np.zeros((2, 2))
	retval[0, 0] = total_mat[0, 0] + total_mat[0, 2] + total_mat[2, 0] + total_mat[2, 2]
	retval[0, 1] = total_mat[0, 1] + total_mat[0, 3] + total_mat[2, 1] + total_mat[2, 3]
	retval[1, 0] = total_mat[1, 0] + total_mat[1, 2] + total_mat[3, 0] + total_mat[3, 2]
	retval[1, 1] = total_mat[1, 1] + total_mat[1, 3] + total_mat[3, 1] + total_mat[3, 3]
	return retval


def main(input_log, output):

	observed, predicted = read_log(input_log)
	datanum = len(observed)
	true_false_mat = np.zeros((4, 4))

	for idx in range(datanum):
		irow = int(observed[idx, 0] * 2 + observed[idx, 1])
		icol = int(predicted[idx, 0] * 2 + predicted[idx, 1])
		true_false_mat[irow, icol] += 1
	
	with open(output, 'w') as ofs:
		ofs.write("[Label Frequency]\n")
		ofs.write("{0:*>10s} PREDICTED_00 PREDICTED_01 PREDICTED_10 PREDICTED_11\n".format(""))
		ofs.write("OBSERVED_00 {0:11d} {1:11d} {2:11d} {3:11d}\n".format(int(true_false_mat[0, 0]), int(true_false_mat[0, 1]), int(true_false_mat[0, 2]), int(true_false_mat[0, 3])))
		ofs.write("OBSERVED_01 {0:11d} {1:11d} {2:11d} {3:11d}\n".format(int(true_false_mat[1, 0]), int(true_false_mat[1, 1]), int(true_false_mat[1, 2]), int(true_false_mat[1, 3])))
		ofs.write("OBSERVED_10 {0:11d} {1:11d} {2:11d} {3:11d}\n".format(int(true_false_mat[2, 0]), int(true_false_mat[2, 1]), int(true_false_mat[2, 2]), int(true_false_mat[2, 3])))
		ofs.write("OBSERVED_11 {0:11d} {1:11d} {2:11d} {3:11d}\n".format(int(true_false_mat[3, 0]), int(true_false_mat[3, 1]), int(true_false_mat[3, 2]), int(true_false_mat[3, 3])))

		true_false_mat /= np.sum(true_false_mat)
		ofs.write("\n[Label Probability]\n")
		ofs.write("{0:*>10s} PREDICTED_00 PREDICTED_01 PREDICTED_10 PREDICTED_11\n".format(""))
		ofs.write("OBSERVED_00 {0:11f} {1:11f} {2:11f} {3:11f}\n".format(float(true_false_mat[0, 0]), float(true_false_mat[0, 1]), float(true_false_mat[0, 2]), float(true_false_mat[0, 3])))
		ofs.write("OBSERVED_01 {0:11f} {1:11f} {2:11f} {3:11f}\n".format(float(true_false_mat[1, 0]), float(true_false_mat[1, 1]), float(true_false_mat[1, 2]), float(true_false_mat[1, 3])))
		ofs.write("OBSERVED_10 {0:11f} {1:11f} {2:11f} {3:11f}\n".format(float(true_false_mat[2, 0]), float(true_false_mat[2, 1]), float(true_false_mat[2, 2]), float(true_false_mat[2, 3])))
		ofs.write("OBSERVED_11 {0:11f} {1:11f} {2:11f} {3:11f}\n".format(float(true_false_mat[3, 0]), float(true_false_mat[3, 1]), float(true_false_mat[3, 2]), float(true_false_mat[3, 3])))

		tf_mat_class0 = true_false_class0(true_false_mat)
		tf_mat_class1 = true_false_class1(true_false_mat)

		accuracy0 = calculate_accuracy(tf_mat_class0)
		ofs.write("\n[Prediction Accuracy Class 0]\n")
		ofs.write("accuracy: {0:10f}\n".format(accuracy0))

		sensitivity_0_0 = calculate_sensitivity(tf_mat_class0, 0)
		sensitivity_0_1 = calculate_sensitivity(tf_mat_class0, 1)
		ofs.write("\n[Prediction Sensitivity Class 0\n]")
		ofs.write("label_0: {0:10f}\n".format(sensitivity_0_0))
		ofs.write("label_1: {0:10f}\n".format(sensitivity_0_1))

		precision_0_0 = calculate_precision(tf_mat_class0, 0)
		precision_0_1 = calculate_precision(tf_mat_class0, 1)
		ofs.write("\n[Prediction Precision Class 0\n")
		ofs.write("label_0: {0:10f}\n".format(precision_0_0))
		ofs.write("label_1: {0:10f}\n".format(precision_0_1))

		accuracy1 = calculate_accuracy(tf_mat_class1)
		ofs.write("\n[Prediction Accuracy Class 1]\n")
		ofs.write("accuracy: {0:10f}\n".format(accuracy1))

		sensitivity_1_0 = calculate_sensitivity(tf_mat_class1, 0)
		sensitivity_1_1 = calculate_sensitivity(tf_mat_class1, 1)
		ofs.write("\n[Prediction Sensitivity Class 1\n]")
		ofs.write("label_0: {0:10f}\n".format(sensitivity_1_0))
		ofs.write("label_1: {0:10f}\n".format(sensitivity_1_1))

		precision_1_0 = calculate_precision(tf_mat_class1, 0)
		precision_1_1 = calculate_precision(tf_mat_class1, 1)
		ofs.write("\n[Prediction Precision Class 1\n")
		ofs.write("label_0: {0:10f}\n".format(precision_1_0))
		ofs.write("label_1: {0:10f}\n".format(precision_1_1))



if __name__ == "__main__":

	import argparse

	parser = argparse.ArgumentParser(description = "Validation routine of a nn model")
	parser.add_argument("--predict_log", help = "path to log file of prediction", required = True)
	parser.add_argument("--output", help = "path to output file", required = True)
	args = parser.parse_args()

	main(args.predict_log, args.output)
