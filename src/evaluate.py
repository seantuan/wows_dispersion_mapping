"""
Evaluation program
Testing data contain video clips and corresponding label csv file
Column of csv file: "x", "y", using opencv coordinate system
"""
import os
import cv2
import csv
import numpy as np
from scipy.optimize import linear_sum_assignment
from argparse import ArgumentParser
from utils.shell import Shell, Point
from utils.helper import measureFuso, rescaleData
from utils.mapping import mapping


if __name__ == '__main__':
	ap = ArgumentParser()
	ap.add_argument('-d', '--dir', required=True, help="directory of testing data")
	args = ap.parse_args()

	assert os.path.isdir(args.dir), "Input directory unavailable"

	videos = [os.path.join(args.dir, f) for f in [f_ for f_ in os.listdir(args.dir) if f_.endswith('.mov') or f_.endswith('.mp4')]]
	annotations = [os.path.join(args.dir, f) for f in [f_ for f_ in os.listdir(args.dir) if f_.endswith('.csv')]]
	
	assert len(videos) == len(annotations), "Numbers of videos and annotations file do not match"

	videos.sort()
	annotations.sort()
	testdata = list(zip(videos, annotations))
	errors = list()
	total_shells = 0
	detected_shells = 0

	for data in testdata:
		video_filename, annotation_filename = data

		# detection
		cap = cv2.VideoCapture(video_filename)
		points = list()
		_, snapshot = cap.read()
		fuso_length, fuso_box = measureFuso(snapshot)
		mapping(cap, points)
		cap.release()

		rescaleData(points, fuso_length)
		total_shells += len(points)		

		# annotation
		true_points = list()
		with open(annotation_filename, newline='') as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				true_points.append(Point([int(row['x']), 0, int(row['y']), 0]))

		rescaleData(true_points, fuso_length)
		detected_shells += len(true_points)

		# Hungarian algorithm
		dim = max([len(true_points), len(points)])
		costs = np.zeros((dim, dim))
		for i, p in enumerate(true_points):
			for j, tp in enumerate(points):
				costs[i][j] = np.linalg.norm(np.array([tp.x, tp.y]) - np.array([p.x, p.y]))
			if len(points) < dim:
				for j in range(len(points), dim):
					costs[i][j] = max(costs[i]) # dummy

		row_idx, col_idx = linear_sum_assignment(costs)
		for i in row_idx:
			if col_idx[i] > len(points) - 1:
				# true points > detected points
				pass

			elif row_idx[i] > len(true_points) - 1:
				# true points < detected points (usually this won't happen)
				pass

			else:
				# normal condition
				errors.append(costs[row_idx[i]][col_idx[i]])


	print("Total shells in the test data: {}".format(total_shells))
	print("Total shells detected by the algorithm: {}".format(detected_shells))
	print("Mean of error: {}".format(np.mean(np.array(errors))))
	print("Std of error: {}".format(np.std(np.array(errors))))

