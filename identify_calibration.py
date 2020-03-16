import numpy as np
import cv2
import pyzbar.pyzbar as zbar
import os
from multiprocessing import Pool
from point import Point, newPoint
from calibration import calibrate

x = 1.15 #units mm
CAL2REAL = [(-x,x,-2*x),(x,x,-2*x),(-x,-x,-2*x),(x,-x,-2*x),(2*x,x,-x),(2*x,x,x),(2*x,-x,-x),(2*x,-x,x),(x,2*x,-x),(x,2*x,x),(-x,2*x,-x),(-x,2*x,x),
	(x,-2*x,-x),(x,-2*x,x),(-x,-2*x,-x),(-x,-2*x,x),(x,x,2*x),(-x,x,2*x),(x,-x,2*x),(-x,-x,2*x),(-2*x,x,x),(-2*x,x,-x),(-2*x,-x,x),(-2*x,-x,-x)
]

pointSchema = [ 'world', 'camera', 'pixel', 'projectedPixel', 'distortedPixel', 'sensor', 'projectedSensor', 'distortedSensor', 'normal', 'projectedNormal', 'distortedNormal' ]

def qr_scan(im):
	"""
	Function for scanning image for QR Codes
	"""
	qr = zbar.decode(im,symbols=[zbar.ZBarSymbol.QRCODE])
	return qr


def identify_points(filename):
	"""
	Find points of calibration object in image
	"""
	points = {}
	images = []

	in_im = cv2.imread(filename)
	in_im = cv2.cvtColor(in_im, cv2.COLOR_BGR2GRAY)
	im = in_im.copy()
	cv2.normalize(in_im,  im, 0, 255, cv2.NORM_MINMAX)
	images.append(im)
	for i in range(10,20):
		r,binary1 = cv2.threshold(im,i*10,255,cv2.THRESH_BINARY)
		images.append(binary1.copy())
	binary2 = cv2.adaptiveThreshold(im,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
	images.append(binary2)

	pool = Pool(20)
	image_qrs = pool.map(qr_scan,images)

	for qrs in image_qrs:
		for qr in qrs:
			poly = qr.polygon
			x,y = 0,0
			for point in poly:
				x+= point.x
				y+= point.y
			x,y = int(x/4),int(y/4)   #<=== Could be bad approximation, may change later
			try:
				points[str(int(qr.data))] = (x,y)
			except:
				print("Invalid QR Code")
	return points


def get_shared(points1, points2):
	"""
	Helper function for getting shared points between cameras
	"""
	camera_1 = set(points1.keys())
	camera_2 = set(points2.keys())
	return list(camera_1.intersection(camera_2))

def point_dict_to_points(point_dict):
	points = []
	for key,item in point_dict.items():
		world_coords = CAL2REAL[int(key)-1]
		sensor_coords = item
		point = newPoint({'world':world_coords,'sensor':sensor_coords})
		points.append(point)
	return points


if __name__ == "__main__":

	data_dir = "data/rubix"
	data_files = ["1.jpg","2.jpg"]

	cpoints = []
	shared = []

	for data_file in data_files:
		filename = os.path.join(data_dir,data_file)
		cpoints.append(identify_points(filename))	
	
	camera_points = []
	for cpoint in cpoints:
		camera_points.append(point_dict_to_points(cpoint))
	
	for camera in camera_points:
		print(calibrate(camera))