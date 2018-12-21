import os
import numpy as np
import json
from argparse import ArgumentParser
from utils.shell import Shell, Point
from utils.helper import excludeOutliers, rescaleData, rotateData, saveCalibratedData, saveCalibratedDataCsv


if __name__ == '__main__':
	ap = ArgumentParser()
	ap.add_argument('-j', '--json', required=True, help="path of json file")
	args = ap.parse_args()

	assert os.path.isfile(args.json), "Input json file unavailable"

	with open(args.json, 'r') as file:
		data = json.load(file)
		fuso_length = data['fuso_length']

	points = []
	for p in data['points']:
		points.append(Point([p['x'], p['dx'], p['y'], p['dy']]))

	excludeOutliers(points)
	rescaleData(points, fuso_length)
	rotateData(points)
	saveCalibratedData(os.path.splitext(args.json)[0] + '_calibrated.json', points)
	saveCalibratedDataCsv(os.path.splitext(args.json)[0] + '_calibrated.csv', points)