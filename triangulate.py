"""
@Author: Cole Hill <coleh@mail.usf.edu>
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
	higher[:dim-1] = lower
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
		V = R.T@np.linalg.pinv(K)@point
		vj = V/np.linalg.norm(V)

		#Store cj and vj
		c.append(cj)
		v.append(vj)

	#Matricies to hold two sums
	A = np.zeros(1)
	B = np.zeros(3)

	#Iterate through (cj,vj) pairs and add
	#Calculations to A and B
	for ci,vi in zip(c,v):
		inter = np.ones(1) - vi@vi.T
		A = A + inter
		B = B + inter*ci

	#Triangulate point
	return (1/A)*B


		