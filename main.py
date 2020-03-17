from triangulate import triangulate_point
from identify_calibration import tsai_calibration
from multiprocessing import freeze_support

if __name__ == "__main__":
	freeze_support()
	image1 = r"C:\Users\Jaime\Desktop\Camera_Calibration\data\rubix\3.jpg"
	point1 = (2467,1279)
	print("Calibrating Camera 1")
	camera1 = tsai_calibration(image1)
	camera1['point'] = point1

	print("Calibrating Camera 2")
	image2 = r"C:\Users\Jaime\Desktop\Camera_Calibration\data\rubix\4.jpg"
	point2 = (1999,1528)
	camera2 = tsai_calibration(image2)
	camera2['point'] = point2

	cameras = [camera1,camera2]

	world_point = triangulate_point(cameras)
	print(world_point)


