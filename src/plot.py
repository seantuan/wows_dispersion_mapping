import os
import numpy as np
import json
import random
from argparse import ArgumentParser
import matplotlib.pyplot as plt

if __name__ == '__main__':
	ap = ArgumentParser()
	ap.add_argument('-j', '--json', required=True, help="path of json file")
	args = ap.parse_args()

	assert os.path.isfile(args.json), "Input json file unavailable"

	with open(args.json, 'r') as file:
		data = json.load(file)
		points = data['points']

	# randomly choose 180
	random.seed(30)
	if len(points) > 180:
		points = random.sample(points, 180)

	xs = np.array([point['x'] for point in points])
	ys = np.array([point['y'] for point in points])

	fig, axs = plt.subplots(2, 1, sharey=True, tight_layout=True, figsize=[8, 8])
	axs[0].hist(xs, bins=100)
	axs[0].set_xlabel('Distance (m)')
	axs[0].set_ylabel('Number of shots')
	axs[0].set_title('Vertical')
	axs[1].hist(ys, bins=100)
	axs[1].set_xlabel('Distance (m)')
	axs[1].set_ylabel('Number of shots')
	axs[1].set_title('Horizontal')
	plt.savefig(os.path.splitext(args.json)[0] + '_histogram.png')
	plt.show()

	fig, ax = plt.subplots(tight_layout=True, figsize=[8, 4])
	ax.scatter(xs, ys, alpha=0.25, c='r')
	ax.set_xlabel('Vertical')
	ax.set_ylabel('Horizontal')
	ax.axis('equal')
	plt.savefig(os.path.splitext(args.json)[0] + '_scatterplot.png')
	plt.show()
