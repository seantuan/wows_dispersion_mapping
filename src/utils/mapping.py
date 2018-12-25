import cv2
import numpy as np
from filterpy.stats import mahalanobis
from scipy.optimize import linear_sum_assignment
from .shell import Shell, Point
from .helper import drawCrosshairs, drawEllipse

def mapping(capture, points):
	lower_color = np.array([0, 100, 100])
	upper_color = np.array([30, 255, 255])

	shells = []
	width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
	height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
	frame_total = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
	frame_count = 1
	previous_img = [np.zeros((height, width), dtype=np.uint8) for _ in range(2)]
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))

	while(capture.isOpened()):
		ret, frame = capture.read()
		if ret == False: break
		frame_count += 1
		
		img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		img = cv2.inRange(img, lower_color, upper_color)
		img = cv2.dilate(img, kernel)
		mask = cv2.bitwise_or(previous_img[0], previous_img[1])
		mask = cv2.dilate(mask, kernel)
		mask = cv2.bitwise_and(cv2.bitwise_not(mask), img)
		mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
		_, contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

		measurements = []
		for cnt in contours:
			moment = cv2.moments(cnt)
			cx = int(moment['m10']/moment['m00'])
			cy = int(moment['m01']/moment['m00'])
			cv2.circle(frame, (cx, cy), 2, (0, 0, 255), -1)
			measurements.append([cx, cy])

		for shell in shells:
			shell.predict()

		# Hungarian algorithm
		dim = max([len(shells), len(measurements)])
		costs = np.zeros((dim, dim))
		for i, shell in enumerate(shells):
			for j, measurement in enumerate(measurements):
				costs[i][j] = np.linalg.norm(np.array([measurement[0], measurement[1]]) - np.array(shell.pos()))
			if len(measurements) < dim:
				for j in range(len(measurements), dim):
					costs[i][j] = max(costs[i]) # dummy

		row_idx, col_idx = linear_sum_assignment(costs)
		for i in row_idx:
			if col_idx[i] > len(measurements) - 1:
				# lose track of shell
				pass

			elif row_idx[i] > len(shells) - 1:
				# new shell
				cx, cy = measurements[col_idx[i]][0], measurements[col_idx[i]][1]
				if width/6 < cx < width*5/6 and height/6 < cy < height*5/6:
					break

				shell = Shell()
				shell.predict()
				shell.update(z=[cx, cy])
				shells.append(shell)

			else:
				# normal condition
				cx, cy = measurements[col_idx[i]][0], measurements[col_idx[i]][1]
				if mahalanobis(x=[cx, cy], mean=shells[row_idx[i]].pos(), cov=shells[row_idx[i]].cov()) < 8:
					shells[row_idx[i]].update(z=[cx, cy])

		# lost track
		for shell in shells:
			if shell.losts > 6:
				if len(shell.xs) > 40:
					point = Point(shell.xs[len(shell.xs) - 1], shell.color)
					points.append(point)
				shells.remove(shell)
		
		# draw frame
		for shell in shells:
			for x in shell.xs:
				cv2.circle(frame, (int(x[0]), int(x[2])), 2, shell.color, -1)
			drawEllipse(frame, shell.pos(), shell.cov())

		for point in points:
			drawCrosshairs(frame, int(point.x), int(point.y), point.color)

		cv2.putText(frame, "shots: {}".format(len(points)), (10, 20), 1, 1, (0, 255, 0), 1, cv2.LINE_AA)
		cv2.putText(frame, "frames: {}/{}".format(frame_count, frame_total), (10, 40), 1, 1, (0, 255, 0), 1, cv2.LINE_AA)

		previous_img[1] = previous_img[0].copy()
		previous_img[0] = img.copy()

		cv2.imshow('frame', frame)
		if cv2.waitKey(1) & 0xFF == ord('q'): break

	cv2.destroyAllWindows()
