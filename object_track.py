'''
@creator: Thomas Theil
@date 19-6-19
@description: This is the class that tracks a color

'''
import cv2
import numpy as np
#from collections import deque


print("Booting");


class track_obj:
	
	def __del__(self):
		cv2.destroyWindow(self.name)
	
	def stop(self):
		cv2.destroyWindow(self.name)
	
	def __init__(self, cap, name):
		self.name = name
		
		
		self.upper = (0, 0, 0)	#lower set of colors
		self.lower = (0, 0, 0)	#upper sets of colors values
		self.color = (0,0,0) 	#the color that the users selected
		
		self.cap = cap			#the camera
		self.frame = cap.read() #read a frame
		self.ball_height =0 	#the height of the obj in procent
		self.screen =0 			#the type of display
	
		
	def track(self):
		ret, frame = self.cap.read()
		
		#blur the screen
		blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)
		self.hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)
	
		#dialte and erode the frames
		self.hsv = cv2.dilate(self.hsv, None, iterations=3)
		self.hsv = cv2.erode(self.hsv, None, iterations=3)


		# maks the image
		mask = cv2.inRange(self.hsv, self.lower, self.upper)		
		contours,h = cv2.findContours(mask,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_NONE)
		area = 0
				
		# only proceed if at least one contour was found
		try:
			if len(contours) > 0:
			
				for cnt_tmp in contours:
					approx_tmp = cv2.approxPolyDP(cnt_tmp, .03 * cv2.arcLength(cnt_tmp, True), True)
					area_tmp = cv2.contourArea(cnt_tmp)
					if(area_tmp > area):
						self.approx = approx_tmp
						area = area_tmp
						self.cnt = cnt_tmp
		
					
				#check if the size is not to big
				if len(self.approx) > 2 and len(self.approx) < 10:
					
					(cx, cy), radius = cv2.minEnclosingCircle(self.cnt)
					
					M = cv2.moments(area)
					if area > 0:
						center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
						circleArea = radius * radius * np.pi
						colors = (int(self.color[0]), int(self.color[1]), int(self.color[2]))
						cv2.circle(frame, (int(cx), int(cy)), int(radius), colors , 5)
						self.ball_height = cy

		except TypeError:
			print("error")

					
		if self.screen is 0:
			self.frame = frame
		else:
			self.frame = mask

	

	
	def screen_event(self,event,x,y,flags,param):
		
		#change the color for the tracker
		if event == 4: #right mouse button
			hsv_color = self.hsv[y , x]
			self.color = self.frame[y , x]
			self.lower = (hsv_color - np.array([4,10,50])).clip(0,255)
			self.upper = (hsv_color + np.array([4,150,200])).clip(0,255)
		#change the screen type
		if event == 5: #left mouse button
			if self.screen is 0:
				self.screen = 1
			else:
				self.screen = 0
		
	def display(self):
		cv2.namedWindow(self.name, cv2.WINDOW_NORMAL)
		cv2.setMouseCallback(self.name, self.screen_event)
		cv2.imshow(self.name, self.frame)

	
	def output(self):
		ball_procent =0 
		
		#procent calculation
		if self.ball_height > 0:
			height = np.size(self.frame, 0)
			one_procent_height = height/100
			ball_procent = 100-(self.ball_height/one_procent_height)

		
		return int(ball_procent)
