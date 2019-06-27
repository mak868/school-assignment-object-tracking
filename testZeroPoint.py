import serial
import time

arduino = serial.Serial("COM2", 9600)
time.sleep(1)
value = 100


while (True):
    print(value)
    arduino.write((str(value) + "\n").encode())
    inFromUser = input("Enter p for plus, m for min and x for exit: ")
    print("\n")
    if (inFromUser == "p"):
        value = value + 1
        if (value > 255):
            value = 255

    elif (inFromUser == "m"):
        value = value - 1
        if (value < 0):
            value = 0

    elif (inFromUser == "x"):
        break

    else:
        print("invalid input: {} \n".format(inFromUser))