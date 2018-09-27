import os
import numpy as np
import json
from argparse import ArgumentParser
from utils.helper import excludeOutliers, calibrateData, saveCalibratedData


def processData():
	ap = ArgumentParser()
	ap.add_argument('-j', '--json', required=True, help="path of json file")
	args = ap.parse_args()

	assert os.path.isfile(args.json), "Input json file unavailable"

	with open(args.json, 'r') as file:
		data = json.load(file)
		points = data['points']
		fuso_length = data['fuso_length']

	excludeOutliers(points)
	calibrateData(points, fuso_length)
	saveCalibratedData(os.path.splitext(args.json)[0] + '_calibrated.json', points)
	

if __name__ == '__main__':
	processData()