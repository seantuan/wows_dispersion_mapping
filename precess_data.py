import os
import cv2
import numpy as np
import json
import random
from argparse import ArgumentParser
import matplotlib.pyplot as plt
from utils.helper import isNotOutlier


if __name__ == '__main__':
	ap = ArgumentParser()
	ap.add_argument('-j', '--json', required=True, help="path of json file")
	args = ap.parse_args()

	assert os.path.isfile(args.json), "Input json file unavailable"

	with open(args.json, 'r') as file:
		data = json.load(file)
		points = data['points']
		fuso_length = data['fuso_length']

	directions = np.array([np.arctan2(-point['dy'], abs(point['dx'])) for point in points])
	xs = np.array([point['x'] for point in points])
	ys = np.array([point['y'] for point in points])

	# exclude outliers
	points = [point for point in points if isNotOutlier(np.arctan2(-point['dy'], abs(point['dx'])), directions, 1)]
	points = [point for point in points if isNotOutlier(point['x'], xs, 3)]
	points = [point for point in points if isNotOutlier(point['y'], ys, 3)]
