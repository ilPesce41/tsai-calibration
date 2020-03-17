"""
@Author: Cole Hill
@Date: 03/17/2020
University of South Florida
"""

import numpy as np


def toHomogenous(point):
	"""
	Convert point to Homogeneous Coordinates
	"""
	dim = len(point)+1
	lower = np.array(point)
	higher = np.ones(dim)
	higher[:dim] = lower
	return higher


def triangulate_point(cameras):
	"""
	Triangulates the real world location of a point
	given pixel locations and calibrated camera models
	"""
	#Two vectors needed in triangulation calculation
	c = []
	v = []

	#Iterate through cameras
	for camera in cameras:

		#Camera calibration
		R = camera['R']
		t = camera['t']
		K = camera['K']

		#Pixel location in homogeneous coordinates
		point = toHomogenous(camera['point'])

		#Calculate cj and vj for  point
		cj = R.T@t
		V = R.T@np.linalg(K)@point
		v = V/np.linalg.norm(V)

		#Store cj and vj
		c.append(c)
		v.append(v)

	#Matricies to hold two sums
	A = np.zeros(3,3)
	B = np.zeros(3)

	#Iterate through (cj,vj) pairs and add
	#Calculations to A and B
	for ci,vi in zip([ci,vi]):
		inter = np.ones((3,3)) - v@v.T
		A = A + inter
		B = B + inter@c

	#Triangulate point
	return np.linalg.inv(A)@B


		