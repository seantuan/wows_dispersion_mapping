import numpy as np
from filterpy.common import Q_discrete_white_noise
from filterpy.kalman import KalmanFilter


def cv_tracker(Q_std=0.1, R_std=0.01, dt=1):
	kf = KalmanFilter(dim_x=4, dim_z=2)
	kf.F = np.array([[1, dt, 0,  0],
					 [0,  1, 0,  0],
					 [0,  0, 1, dt],
					 [0,  0, 0,  1]], dtype=float)
	kf.H = np.array([[1, 0, 0, 0],
					 [0, 0, 1, 0]], dtype=float)
	kf.x = np.array([0, 1, 0, 1], dtype=float) # initial state
	kf.P = np.diag([30**2, 3**2, 30**2, 3**2]) # initial uncertainty
	q = Q_discrete_white_noise(dim=2, dt=dt, var=Q_std**2)
	kf.Q[0:2, 0:2] = q
	kf.Q[2:4, 2:4] = q
	kf.R *= R_std**2
	return kf
