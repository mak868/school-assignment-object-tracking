'''
@creator: Thomas Theil
@date 14-6-19
@description: This code wil track the larges object on the seen

'''

from tkinter import *
from object_track import *
import time
#import serial

#start tikinter windo
window = Tk()
window.title("Track Objects") 

#serial
#ser = serial.Serial('COM3', 9600)

#start video capter
cap = cv2.VideoCapture(0)
time.sleep(2) #give the camera some time to warm up

tracking_list = [] #list of all the trackted objects
tracking_value= [] #list of all the values of the objects

arduino_out = False



#add a new object that needs to be trackted
def add_obj():
	name = "obj "+ str(len(tracking_list))
	tracking_list.append(track_obj(cap, name))
	tracking_value.append(0)

#remove the last of the tracked objects
def remove_obj():
	if len(tracking_list) != 0:
	
		#stoping the screen
		obj_tmp = tracking_list[-1]
		obj_tmp.stop()
		del obj_tmp
		
		#removing the data from the array
		tracking_list.pop()
		tracking_value.pop()
		




	

#loop true all the objects that are track
def loop_tack():
	i=0
	for obj in tracking_list:
		obj.track()
		obj.display()			
		tracking_value[i]= obj.output()
		i +=1
	window.after(10, loop_tack) #loop this code every 10e of a second 
	
	#output for the arduino
	if arduino_out is True:
		arduino_output()

	
#output for the terminal	
def terminal_output():
	if len(tracking_value) > 0:
		print(*tracking_value)
	window.after(output_speed, terminal_output) #loop for output data

#output for the arduino
def arduino_output():
	# first where the ball needs to be
	# second where the ball is
	if len(tracking_value) is 0:
		list = (0, 0)
	elif len(tracking_value) is 1:	
		list = (tracking_value[1], tracking_value[0])
		
	elif len(tracking_value) is 2:
		list = (tracking_value[1], tracking_value[0])
	
	output = '|'.join(map(str, list))
	print(output)
	#ser.write(output)

def arduino_loop():
	global arduino_out
	if arduino_out:
		arduino_out = False
	else:
		arduino_out = True


#start up the endless loop time scadule
window.after(50, loop_tack) #loop for the camera color tracking


#add buttons to wind
bnt = Button(window, text="Add a extra tracked object", command=add_obj)
bnt.grid(column=1, row=0)

bnt = Button(window, text="Remove track object", command=remove_obj)
bnt.grid(column=1, row=1)


bnt = Button(window, text="set screen obj one to position obj two", command=arduino_loop)
bnt.grid(column=1, row=2)



#window main loop
window.mainloop()

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
