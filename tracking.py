'''
@creator: Thomas Theil
@date 14-6-19
@description: This code wil track the larges object on the seen

'''
import numpy as np
from collections import deque
import argparse
import cv2
import time
import imutils

cap = cv2.VideoCapture(0)
time.sleep(2)

balltrack_Lower = (5, 50, 50)  		#lower set of colors
balltrack_Upper = (15, 255, 255)	#upper sets of colors values
average = 5 #the average vor smothing the output



#don't edit this var these are use as tmp or counters
average_count =0
average_calc =0
ball_height= 0
ball_procent =0
height =0
output =0


while(True):
    # Capture frame-by-frame
	ret, frame = cap.read()
	height = np.size(frame, 0)

	blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)
	hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)
	
	#dialte and erode the frames
	hsv = cv2.dilate(hsv, None, iterations=4)	
	hsv = cv2.erode(hsv, None, iterations=3)
	
	# maks the image
	mask = cv2.inRange(hsv, balltrack_Lower, balltrack_Upper)		
	contours,h = cv2.findContours(mask,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_NONE)
	area = 0
	
	
	# only proceed if at least one contour was found
	if len(contours) > 0:
		
		for cnt_tmp in contours:
			approx_tmp = cv2.approxPolyDP(cnt_tmp, .03 * cv2.arcLength(cnt_tmp, True), True)
			area_tmp = cv2.contourArea(cnt_tmp)
			if(area_tmp > area):
				approx = approx_tmp
				area = area_tmp
				cnt = cnt_tmp
		

		#check if the size is not to big
		if len(approx) > 4 and len(approx) < 10:
			
			(cx, cy), radius = cv2.minEnclosingCircle(cnt)
			
			M = cv2.moments(area)
			if area > 0:
				center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
				circleArea = radius * radius * np.pi
				cv2.circle(frame, (int(cx), int(cy)), int(radius),(255, 0, 0), -1)
				ball_height = cy

					
	
	
			
	# Display the resulting frame
	cv2.imshow('frame', frame)
	cv2.imshow("Mask", mask)

	#procent calculation
	if ball_height > 0:
		one_procent_height = height/100
		ball_procent = 100-(ball_height/one_procent_height)

		
	#caculate to 0 till 255
	if ball_procent > 0:
		pid_out_tmp = int(ball_procent*2.55) #caculate the procent to a char
	else:
		pid_out_tmp = 0
	

	#averaging the data
	if average_count < average:
		average_count +=1
		average_calc += pid_out_tmp
	else:
		pid_out = int(average_calc/average)
		average_calc = 0
		average_count =0
	
	
	
	print(output) #output data
	
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
