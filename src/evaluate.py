"""
Evaluation program
Testing data contain video clips and corresponding label csv file
Column of csv file: "x", "y", using opencv coordinate system
"""
import os
import cv2
import numpy as np
from argparse import ArgumentParser
from utils.shell import Shell, Point
from utils.helper import measureFuso
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

	for data in testdata:
		video_filename, annotation_filename = data

		cap = cv2.VideoCapture(video_filename)
		points = list()
		_, snapshot = cap.read()
		fuso_length, fuso_box = measureFuso(snapshot)
		mapping(cap, points)
		cap.release()

		true_points = list()
		with open(annotation_filename, newline='') as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				true_points.append(Point([row['x'], row['y'], 0, 0]))


