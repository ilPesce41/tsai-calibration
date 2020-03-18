from triangulate import triangulate_point
from identify_calibration import tsai_calibration
from multiprocessing import freeze_support
import sys

if __name__ == "__main__":

	freeze_support()
	

	args = sys.argv
	config_file = args[1]
	try:
		lines = open(config_file).readlines()
		lines = [x.replace('\n','') for x in lines]
	except Exception as e:
		print("Invalid input File")
		print(e)
		sys.exit()
	if len(lines)<4:
		print("Not enough entries in input file")
	image1 = lines[0]
	
	print("Calibrating Camera 1")
	camera1 = tsai_calibration(image1)

	print("Calibrating Camera 2")
	image2 = lines[1]
	camera2 = tsai_calibration(image2)


	point1 = tuple(map(int,lines[2].split(',')))
	point2 = tuple(map(int,lines[3].split(',')))	
	camera1['point'] = point1
	camera2['point'] = point2
	cameras = [camera1,camera2]
	world_point = triangulate_point(cameras)
	print(world_point)
