import random
import numpy as np
from .tracker import cv_tracker


class Shell:
	def __init__(self):
		self.tracker = cv_tracker(Q_std=0.07, R_std=1.5, dt=1)
		self.xs = []
		self.losts = 0
		self.color = (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

	def predict(self):
		self.tracker.predict()
		self.losts += 1

	def update(self, z):
		self.tracker.update(np.array(z))
		self.xs.append(self.tracker.x.copy())
		self.losts = 0

	def pos(self):
		return [self.tracker.x[0], self.tracker.x[2]]

	def speed(self):
		return [self.tracker.x[1], self.tracker.x[3]]

	def cov(self):
		return [[self.tracker.P[0, 0], self.tracker.P[0, 2]],
				[self.tracker.P[2, 0], self.tracker.P[2, 2]]]


class Point:
	def __init__(self, X, color=None):
		self.x = X[0]
		self.y = X[2]
		self.dx = X[1]
		self.dy = X[3]
		self.color = color
