import tensorflow as tf
from tensorflow import keras
from iomanip import read_two_label_dataset
from util import util_decimal
import numpy as np
import matplotlib.pyplot as plt
import sys
import math
import subprocess


def main(dataset_name, model_name, output):

	dataset, labels = read_two_label_dataset(dataset_name, density = False)
	model = keras.models.load_model(model_name)
	# prediction
	predicted = model.predict(dataset)
	predicted = util_decimal(predicted).astype(int)
	if len(predicted) != len(labels):
		print("The size of dataset is not consistent with that of labels")
		sys.exit()
		
	datanum = len(predicted)
	with open(output, 'w') as ofs:
		ofs.write("[PREDICTED] [ANSWER]\n")
		for idx in range(datanum):
			#ofs.write(str(predicted[idx]) + " " +  str(labels[idx]) + "\n")
			ofs.write(str(predicted[idx, 0]) + " " + str(predicted[idx, 1]) + " " + str(labels[idx, 0]) + " " + str(labels[idx, 1]) + "\n")


if __name__ == "__main__":

	import argparse

	parser = argparse.ArgumentParser(description = "Model prediction")
	parser.add_argument("--dataset_path", help = "path to dataset file", required = True)
	parser.add_argument("--model_path", help = "path to the model file", required = True)
	parser.add_argument("--output", help = "path to the output file", required = True)
	args = parser.parse_args()

	main(args.dataset_path, args.model_path, args.output)
