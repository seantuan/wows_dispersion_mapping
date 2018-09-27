import os
import cv2
import numpy as np
from argparse import ArgumentParser
import utils.shell
from utils.helper import measureFuso, saveData, saveSnapshot
from utils.mapping import mapping


if __name__ == '__main__':
	ap = ArgumentParser()
	ap.add_argument('-v', '--video', required=True, help="path of video to read")
	args = ap.parse_args()

	assert os.path.isfile(args.video), "Input video unavailable"

	cap = cv2.VideoCapture(args.video)
	points = []
	_, snapshot = cap.read()
	fuso_length, fuso_box = measureFuso(snapshot)

	mapping(cap, points)

	cap.release()

	saveData(os.path.splitext(args.video)[0] + '.json', points, fuso_length)
	saveSnapshot(os.path.splitext(args.video)[0] + '.jpg', snapshot, points, fuso_box)