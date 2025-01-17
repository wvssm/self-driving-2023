#!/usr/bin/env  python

import sys
import cv2
import numpy as np

import rospy
from cv_bridge import CvBridge

from traffic_light_classifier.msg import traffic_light
from sensor_msgs.msg import Image
from std_msgs.msg import Header

RED = 0
GREEN = 1
UNKNOWN = 2


class BBox(object):
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height


def calculate_bounds(bound):
	xmin = sys.maxint
	xmax = -sys.maxint - 1
	ymin = sys.maxint
	ymax = -sys.maxint - 1

	x = bound.x
	y = bound.y

	xmin = min(xmin, x)
	xmax = max(xmax, x)
	ymin = min(ymin, y)
	ymax = max(ymax, y)

	#xmax = xmin + bound.width
	ymax = ymin + bound.height

	return xmin, xmax, ymin, ymax


def crop_image(image, xmin, xmax, ymin, ymax):
	return image.crop((xmin, ymin, xmax, ymax)) #image.crop((xmin, ymin, xmax, ymax))


def predict_light(cropped_roi):

	return UNKNOWN


def detect_callback(image):
	# refer from : https://github.com/Cilab-kr/TrafficLight-Detector/blob/master/src/main.py
	global bounds, detect_cnt, tl_result

	if bounds.x == 0 and bounds.y == 0:
		# No signals are visible
		traffic_light.recognition_result = UNKNOWN
		light_detected_pub.publish(traffic_light(traffic_light=UNKNOWN))
		return

	if (detect_cnt % 50 != 0):
		detect_cnt += 1
		return

	cv_bridge = CvBridge()
	cimg = cv_bridge.imgmsg_to_cv2(image, "bgr8")
	size = cimg.shape
	cimg = cimg[:, :] #resize
	hsv = cv2.cvtColor(cimg, cv2.COLOR_BGR2HSV)

	# color range
	lower_red1 = np.array([0,100,100])
	upper_red1 = np.array([10,255,255])
	lower_red2 = np.array([160,100,100])
	upper_red2 = np.array([180,255,255])

	#lower_green1 = np.array([40,255,200])
	#upper_green1 = np.array([52,255,255])
	#lower_green2 = np.array([44,70,255])
	#upper_green2 = np.array([46,80,255])
	#lower_green3 = np.array([47,220,37])
	#upper_green3 = np.array([60,255,255])

	lower_green1 = np.array([50,20,200])
	upper_green1 = np.array([52,255,255])
	lower_green2 = np.array([49,43,255]) #60
	upper_green2 = np.array([75,255,255])
	lower_green3 = np.array([50,220,200])
	upper_green3 = np.array([60,255,255])

	#lower_green1 = np.array([40,255,200])
	#upper_green1 = np.array([52,255,255])
	#lower_green2 = np.array([44,10,255])
	#upper_green2 = np.array([46,80,255])
	#lower_green3 = np.array([47,220,37])
	#upper_green3 = np.array([60,255,255])

	lower_yellow = np.array([15,150,150])
	upper_yellow = np.array([35,255,255])
	mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
	mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
	maskg1 = cv2.inRange(hsv, lower_green1, upper_green1)
	maskg2 = cv2.inRange(hsv, lower_green2, upper_green2)
	maskg3 = cv2.inRange(hsv, lower_green3, upper_green3)

	masky = cv2.inRange(hsv, lower_yellow, upper_yellow)
	maskr = cv2.add(mask1, mask2)

	maskgg1= cv2.add(maskg1, maskg2)
	maskg= cv2.add(maskgg1, maskg3)

	# kernel = np.ones((3, 3), np.uint8)
	# maskg = cv2.erode(maskg, kernel, iterations=6)
	# maskg = cv2.dilate(maskg, kernel, iterations=3)

	size = hsv.shape

	# hough circle detect
	r_circles = cv2.HoughCircles(maskr, cv2.HOUGH_GRADIENT, 1, 80,
							   param1=50, param2=5, minRadius=0, maxRadius=30)

	g_circles = cv2.HoughCircles(maskg, cv2.HOUGH_GRADIENT, 1, 50,
								 param1=50, param2=5, minRadius=0, maxRadius=30) #par2 = 5

	y_circles = cv2.HoughCircles(masky, cv2.HOUGH_GRADIENT, 1, 30,
								 param1=50, param2=5, minRadius=0, maxRadius=30)

	# traffic light detect
	red_detected = False
	green_detected = False
	r = 5
	bound = 4.0 / 10
	
	if g_circles is not None: # and not red_detected
		g_circles = np.uint16(np.around(g_circles))

		for i in g_circles[0, :]:
			if i[0] > size[1] or i[1] > size[0] or i[1] > size[0]*bound:
				continue

			h, s = 0.0, 0.0
			for m in range(-r, r):
				for n in range(-r, r):

					if (i[1]+m) >= size[0] or (i[0]+n) >= size[1]:
						continue
					h += maskg[i[1]+m, i[0]+n]
					s += 1
			if h / s > 40:
				cv2.circle(cimg, (i[0], i[1]), i[2]+10, (0, 0, 255), 2)
				traffic_light_result.recognition_result = GREEN
				green_detected = True
				print("GREEN!!!!")

	if not red_detected and not green_detected:
		traffic_light_result.recognition_result = UNKNOWN

	roi_image.publish(cv_bridge.cv2_to_imgmsg(cimg, "bgr8"))
	light_detected_pub.publish(traffic_light_result)


if __name__ == '__main__':
	rospy.init_node('traffic_light_detector', anonymous=True)

	detect_cnt = 0
	traffic_light_result = traffic_light()
	bounds = BBox(x=10, y=10, width=600, height=400)
	predict_sub = rospy.Subscriber('/usb_cam/image_raw', Image, detect_callback, queue_size=1, buff_size=52428800)
	light_detected_pub = rospy.Publisher(
		'light_color', traffic_light, queue_size=5)
	roi_image = rospy.Publisher('roi_image', Image, queue_size=1)

	rospy.spin()
