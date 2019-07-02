'''
@creator: Thomas Theil
@date 14-6-19
@description: This code wil track the larges object on the seen

'''

from tkinter import *
from object_track import *
import time
import serial
from PID_Controller import PID

#vars for ouputing to a display
arduino_out = True  #out to the arduino
data_display = False #send a data output


p_center_obj_status = False #program center object
p_folow_obj = False #program object folow
p_game_mode = False #program game mode
to_pong = 1 #direction of the ball going to the pong bat
pid_value = {'p':2.0, 'i':0.3, 'd':1.0}



#start tikinter windo
window = Tk()
window.title("Track Objects") 



#start video capter
cap = cv2.VideoCapture(1)
time.sleep(2) #give the camera some time to warm up

tracking_list = [] #list of all the trackted objects
tracking_value= [] #list of all the values of the objects


pid = PID()

pid.setKp(pid_value['p'])
pid.setKi(pid_value['i']) #0.3
pid.setKd(pid_value['d'])
pid.setMaxValue(230)



#serial
if(arduino_out): #check if serial com is on or not
	#ser = serial.Serial('COM3', 9600)
	arduino = serial.Serial('COM3', 9600)
	time.sleep(1)
	arduino.write("0\n".encode())


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
	if data_display is True:
		data_out()


	
#output for the terminal	
def terminal_output():
	if len(tracking_value) > 0:
		print(*tracking_value)
	window.after(output_speed, terminal_output) #loop for output data

#output for the arduino
def data_out():

	# first where the ball needs to be
	# second where the ball is
	if len(tracking_value) is 0:
		list = (0, 0)
	elif len(tracking_value) is 1:	
		list = (50, tracking_value[0])
		
	elif len(tracking_value) is 2:
		list = (tracking_value[1], tracking_value[0])
	
	#check if game mode is on 
	if p_game_mode:
		list = mini_game()

	#change pid values
	pid.setKp(scale.get())
	pid.setKi(scale2.get())  # 0.3
	pid.setKd(scale3.get())

	#check if arduino out is on or of
	if arduino_out: #send data to the arduino
		pid.setTarget(list[0])
		pid.process(list[1])
		#output = str(list[0]) + ", " + str(list[1]) + ", " + str(pid.getValue())
		sendvalue = str(pid.getValue()) + '|' + str(tracking_value[0])
		arduino.write((sendvalue + "\n").encode())
		#print(pid.getValue())
	else: #send data to the serial out
		output = '|'.join(map(str, list))
		print(output , scale3.get())


def mini_game():
	global to_pong

	if len(tracking_value) is 3:
		ball =  tracking_value[0]
		pong_one =  tracking_value[1]
		pong_two =  tracking_value[2]

		#change ball direction
		if abs(pong_one - ball) <= 5: #if ball is with in 5% of the pong chang the dir to pong two
			to_pong = 2
		elif abs(ball - pong_two) <= 5: #if ball is with in 5% of the pong chang the dir to pong one
			to_pong = 1

		if to_pong is 1:
			return [ball, pong_one]
		else:
			return [ball,pong_two]

		
	

'''
center object 
this program will center the trackted object
'''
def center_obj():
	global p_center_obj_status
	global data_display

	if not p_center_obj_status:
		add_obj()
		data_display = True
		cnt_track_button.configure(text="Close object center")
		p_center_obj_status = True
	else:
		remove_obj()
		data_display = False
		p_center_obj_status = False
		cnt_track_button.configure(text="object center")

'''
folow object
this program will try to let the ball folow the second trackt object
'''
def folow_obj():
	global p_folow_obj
	global data_display

	if not p_folow_obj:
		add_obj()
		add_obj()
		data_display = True
		p_folow_obj = True
		folow_button.configure(text="Close object center")
	else:
		remove_obj()
		remove_obj()
		data_display = False
		p_folow_obj = False
		folow_button.configure(text="object center")	
		

'''
Game mode is a litle pong game in 1D!.
this game will send the ball between the pongs 
all pongs are trackted objects
'''
def game_mode():
	global p_game_mode
	global data_display

	if not p_game_mode:
		add_obj()
		add_obj()
		add_obj()
		data_display = True
		p_game_mode = True
		game_button.configure(text="Close Game")
	else:
		remove_obj()
		remove_obj()
		remove_obj()
		data_display = False
		p_game_mode = False
		game_button.configure(text="Start game")	


def pid_change():
	print(pid_value['p'])


#start up the endless loop time scadule
window.after(50, loop_tack) #loop for the camera color tracking




#add button to window
cnt_track_button = Button(window, text="object center", command=center_obj)
cnt_track_button.grid(column=1, row=0)



#controle the first obj with a second obj
folow_button = Button(window, text="object folow", command=folow_obj)
folow_button.grid(column=1, row=1)



#play a litle game with 3 trackt obj's 
game_button = Button(window, text="Start game", command=game_mode)
game_button.grid(column=1, row=2)

#scales for changing pid
scale2 = Scale(window, tickinterval=5 , resolution=0.5, from_=0, to=10)
scale2.grid(column=0, row=3)

scale = Scale(window, tickinterval=0.2 , resolution=0.05, from_=0, to=1)
scale.grid(column=1, row=3)

scale3 = Scale(window,tickinterval=5 , resolution=0.5, from_=0, to=20)
scale3.grid(column=2, row=3)

#set the pre values
scale.set(pid_value['p'])
scale2.set(pid_value['i'])
scale3.set(pid_value['d'])

# advanced mode  
if False:
	#add buttons to wind
	bnt = Button(window, text="Add a extra tracked object", command=add_obj)
	bnt.grid(column=1, row=0)

	bnt = Button(window, text="Remove track object", command=remove_obj)
	bnt.grid(column=1, row=1)

	bnt = Button(window, text="set screen obj one to position obj two", command=data_out)
	bnt.grid(column=1, row=2)




#window main loop
window.mainloop()

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
