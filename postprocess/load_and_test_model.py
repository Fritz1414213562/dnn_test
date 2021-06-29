import tensorflow as tf
from tensorflow import keras
from iomanip import read_dataset
from util import util_decimal
import numpy as np
import matplotlib.pyplot as plt
import sys
import math
import subprocess


def main(dataset_name, model_name):

	dataset, labels = read_dataset(dataset_name, density = True)
	model = keras.models.load_model(model_name)
	# prediction
	predicted = model.predict(dataset)
	predicted = predicted.reshape((len(predicted),))
	predicted = util_decimal(predicted).astype(int)
	if len(predicted) != len(labels):
		print("The size of dataset is not consistent with that of labels")
		sys.exit()
		
	datanum = len(predicted)
	print("[PREDICTED]", "[ANSWER]")
	for idx in range(datanum):
		print(predicted[idx], labels[idx])


if __name__ == "__main__":

	import argparse

	parser = argparse.ArgumentParser(description = "Model prediction")
	parser.add_argument("--dataset_path", help = "path to dataset file", required = True)
	parser.add_argument("--model_dir", help = "path to the model dir", required = True)
	args = parser.parse_args()

	main(args.dataset_path, args.model_dir)