#!/usr/bin/env python
# BEGIN ALL
import rospy
import cv2
import cv_bridge
import numpy
import math
from sensor_msgs.msg import Image
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from traffic_light_classifier.msg import traffic_light

global perr, ptime, serr, dt, move, ray_angle
perr = 0
ptime = 0
serr = 0
dt = 0
move = False
angle_step_deg = 20
green_cnt = 0


class Follower:
	def __init__(self):
		self.bridge = cv_bridge.CvBridge()
		self.image_sub = rospy.Subscriber('/usb_cam/image_raw',	Image, self.image_callback)
		self.lidar_sub = rospy.Subscriber('/scan_raw', LaserScan, self.lidar_callback)
		self.traffic_sub = rospy.Subscriber('/light_color', traffic_light, self.traffic_callback)
		self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
		self.image_pub = rospy.Publisher('/lane_image', Image, queue_size=1)
		self.twist = Twist()
		self.ray_angle = [x for x in range(angle_step_deg, 180, angle_step_deg)]
		self.dists = None
		
		self.traffic_color = 0

		self.cmd_vel_pub.publish(self.twist)

	def traffic_callback(self, msg): 
		global move, green_cnt
		self.traffic_color = msg.recognition_result 
		
		if self.traffic_color == 1:
			green_cnt += 1 
			print("Green_cnt :{}".format(green_cnt))

	def lidar_callback(self, msg):
		# get lidar distance at ray_angle in degree
		# dynamic offset
		# angles = [(x - 90) % 360 for x in self.ray_angle]
		# self.dists = [msg.ranges[x*2] for x in angles]
		# self.dists = list(map(lambda x: 0.1 if x == float('inf') else x, self.dists))
		# self.dists = list(map(lambda x: 0.5 if x >= 0.5 else x, self.dists))

		# static offset
		angles = [x for x in range(-1, -80, -1)] #hmm.. 1,3 set chagne plz
		self.dists = [msg.ranges[x*2] for x in angles]

	def get_obstacle_threshold(self):
		if self.dists == None:
			return 0

		# dynamic offset
		# lateral_dists = [dist * numpy.cos(numpy.deg2rad(theta)) for dist, theta in zip(self.dists, self.ray_angle)]

		# static offset
		lateral_count = 0
		for d in self.dists:
			if d < 0.6: #setting 0.58 0.54
				lateral_count += 1
		if lateral_count >= 1: 
			print("lateral_cnt :{}".format(lateral_count))
			return 40 #85
		else:
			return 0

		# dynamic offset
		# return sum(lateral_dists)

	def image_callback(self, msg):
		global perr, ptime, serr, dt
		image0 = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

		# transformation
		img = cv2.resize(image0, None, fx=0.6, fy=0.6,
						 interpolation=cv2.INTER_CUBIC)
		#print img.shape
		rows, cols, ch = img.shape
		pts1 = numpy.float32([[5, 190], [0, 280], [375, 190], [380, 280]])
		pts2 = numpy.float32([[0, 0], [0, 300], [300, 0], [300, 300]])

		cv2.circle(img, (5, 190), 10, (255, 0, 0), -1)
    		cv2.circle(img, (0, 280), 10, (0, 255, 0), -1)
    		cv2.circle(img, (375, 190), 10, (0, 0, 255), -1)
    		cv2.circle(img, (380, 280), 10, (0, 255, 255), -1)


    		mtrx = cv2.getPerspectiveTransform(pts1, pts2)


    		#dst = cv2.warpPerspective(img, mtrx, (300, 300))

    		#cv2.imshow("origin", img)
    		#cv2.imshow("perspective", dst)
    		#cv2.waitKey(0)
    		#cv2.destroyAllWindows()

		M = cv2.getPerspectiveTransform(pts1, pts2)
		img_size = (img.shape[1], img.shape[0])
		image = cv2.warpPerspective(img, M, (300, 300))  # img_size

		hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		
		lower_orangeRed = numpy.array([0, 30, 80])
        	upper_orangeRed = numpy.array([11, 255, 255])

        	lower_pinkRed = numpy.array([150, 30, 80])
        	upper_pinkRed = numpy.array([180, 255, 255])

        	maskor = cv2.inRange(hsv, lower_orangeRed, upper_orangeRed)
       		maskpr = cv2.inRange(hsv, lower_pinkRed, upper_pinkRed)

        	maskr = cv2.bitwise_or(maskor, maskpr)
		
		rgb_r = cv2.bitwise_and(image, image, mask=maskr).astype(numpy.uint8)
        	rgb_r = cv2.cvtColor(rgb_r, cv2.COLOR_RGB2GRAY)


		# filter mask
		#kernel = numpy.ones((7, 7), numpy.uint8)
		#opening = cv2.morphologyEx(rgb_r, cv2.MORPH_OPEN, kernel)
		#rgb_r = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
		#_, rgb_r = cv2.threshold(rgb_r, 210, 255, cv2.THRESH_BINARY)

		#out_img = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

		# ROI
        	out_img = rgb_r.copy()
        	h, w = out_img.shape
        	search_top = int(1 * h / 4 + 20)
        	search_bot = int(3 * h / 4 + 20)
        	search_mid = int(w / 2)
        	out_img[0:search_top, 0:w] = 0
		
		M = cv2.moments(out_img)
		c_time = rospy.Time.now()

		if green_cnt >= 3:
			if M['m00'] > 0:
				cxm = int(M['m10']/M['m00'])
				cym = int(M['m01']/M['m00'])

				# cx = cxm - 110 #120#143 #CW
				#cx = cxm - 150
				offset = self.get_obstacle_threshold()
				#print("offset: ", offset)
				cx = cxm - offset

				cv2.circle(out_img, (cxm, cym), 20, (255, 0, 0), -1)
				cv2.circle(out_img, (cx, cym), 20, (255, 0, 0), 2)

				# BEGIN CONTROL
				err = cx - 4 * w / 8
                		#K_p = 0.8

                		dt = rospy.get_time() - ptime

                		D = ((err - perr) / (rospy.get_time() - ptime)) * 1 / 20 / 100
                		ang_z = (float(err) / 100) * (0.4) + D #0.3
                		ang_z = min(0.8, max(-0.8, ang_z)) #hmm,,,,,,

                		if offset != 0 and abs(ang_z) > 0.05:
                    			K_p = 1.0 #1.0
                		else:
					# K_p = 2.3
					K_p = 1.0 #1.6

                		lin_x = ang_z
                		if lin_x < 0:
                    			lin_x = -(lin_x)
                		lin_x = K_p * (1.0 - lin_x)

                		self.twist.linear.x = lin_x
                		self.twist.angular.z = -ang_z

                		perr = err
                		ptime = rospy.get_time()

			else:
				self.twist.linear.x = 0.1
				self.twist.angular.z = -0.2
				#err = 0

			self.cmd_vel_pub.publish(self.twist)
			output_img = self.bridge.cv2_to_imgmsg(out_img)
			self.image_pub.publish(output_img)

			# END CONTROL

			#cv2.imshow("win3", rgb_yw2)
			# cv2.waitKey(3)


rospy.init_node('follower')
follower = Follower()
rospy.spin()
# END ALL
