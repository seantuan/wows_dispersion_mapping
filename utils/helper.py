import os
import cv2
import json
import numpy as np
from .shell import Shell, Point


def drawCrosshairs(img, cx, cy, color):
	cv2.line(img, (cx - 5, cy), (cx + 5, cy), color, 1)
	cv2.line(img, (cx, cy - 5), (cx, cy + 5), color, 1)


def drawEllipse(img, pos, cov):
	w, v = np.linalg.eig(cov) # get eigenvalues and eigenvectors
	angle = np.arctan2(v[0, 1], v[0, 0])
	if angle < 0:
		angle += 2 * np.pi # shift the angle to the [0, 2pi] interval instead of [-pi, pi]
	angle = np.rad2deg(angle)
	axes = (int(3 * np.sqrt(w[0])), int(3 * np.sqrt(w[1])))
	mean = (int(pos[0]), int(pos[1]))
	cv2.ellipse(img, mean, axes, angle, 0, 360, (255, 0, 0), 1)


def drawTransparentCircle(img, cx, cy, color, alpha):
	overlay = img.copy()
	cv2.circle(img, (cx, cy), 5, color, -1)
	cv2.addWeighted(src1=img, alpha=alpha, src2=overlay, beta=1. - alpha, gamma=0, dst=img)


def measureFuso(frame):
	lower_color = np.array([0, 0, 0])
	upper_color = np.array([180, 255, 60])

	mask = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(mask, lower_color, upper_color)
	mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT,(3, 3)))
	mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT,(5, 5)))
	mask = cv2.erode(mask, cv2.getStructuringElement(cv2.MORPH_RECT,(3, 3)))
	mask = cv2.bitwise_not(mask)
	_, contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	
	max_area = 0.
	max_idx = 0
	for i, cnt in enumerate(contours):
		area = cv2.contourArea(cnt)
		if area > max_area:
			max_idx = i
			max_area = area

	rect = cv2.minAreaRect(contours[max_idx])
	box = np.int0(cv2.boxPoints(rect))
	fuso_length = max([np.linalg.norm(box[0] - box[1]), np.linalg.norm(box[1] - box[2])])
	return fuso_length, box


def saveData(filename, points, fuso_length):
	points_dict = [dict(zip(['x', 'y', 'dx', 'dy'], [point.x, point.y, point.dx, point.dy])) for point in points]
	data = dict({'filename': os.path.splitext(os.path.basename(filename))[0], 'fuso_length': fuso_length, 'points': points_dict})
	with open(filename, 'w') as outfile:
		json.dump(data, outfile, indent=4)


def saveSnapshot(filename, frame, points, fuso_box):
	for point in points:
		drawTransparentCircle(frame, int(point.x), int(point.y), (0, 0, 255), .25)
	cv2.drawContours(frame, [fuso_box], 0, (0, 0, 255), 1)
	cv2.putText(frame, "shots: {}".format(len(points)), (10, 20), 1, 1, (0, 255, 0), 1, cv2.LINE_AA)
	cv2.imwrite(filename, frame)


def isNotOutlier(value, data, m=5):
	return abs(value - np.mean(data)) < m * np.std(data)
