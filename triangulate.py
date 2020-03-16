import numpy as np


def toHomogenous(point):
	dim = len(point)+1
	lower = np.array(point)
	higher = np.ones(dim)
	higher[:dim] = lower
	return higher


def triangulate_point(cameras):
	
	c = []
	v = []

	for camera in cameras:

		R = camera['R']
		t = camera['t']
		K = camera['K']
		point = toHomogenous(camera['point'])
		cj = R.T@t
		V = R.T@np.linalg(K)@point
		v = V/np.linalg.norm(V)
		c.append(c)
		v.append(v)

	A = np.zeros(3,3)
	B = np.zeros(3)
	for ci,vi in zip([ci,vi]):
		inter = np.ones((3,3)) - v@v.T
		A = A + inter
		B = B + inter@c

	return np.linalg.inv(A)@B


		