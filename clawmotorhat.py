from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor #Motor Hat Board
import os     #importing os library so as to communicate with the system
import time   #importing time library to make Rpi wait because its too impatient 
os.system ("sudo pigpiod") #Launching GPIO library
time.sleep(1) # As i said it is too impatient and so if this delay is removed you will get an error
import pigpio #importing GPIO library
import socket
import RPi.GPIO as GPIO #importing GPIO code for the pi

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sets up the server with socket and calling the socket libraries

ip = '10.159.105.123'
#ip = '192.168.1.149'
#sets the ip address for the server which is the pi
port = 5678
#port that you want the client to connect to- can be any number you want

address = (ip, port)
server.bind(address)
#sets the server or pi to that set address and port and binds it

server.listen(2)
#amount of clients connected at a time

print "My pi is listeneing now" ,ip, ":", port
#displaying the address being broadcast by the pi on the terminal
client, addr = server.accept()
#allows the client to connect and be accepted by the server/pi
print "got a connection from ", addr[0], ";", addr[1]
#defined the name and address of the client who connected

mh = Adafruit_MotorHAT(addr=0x6f) #assign I2C port for default pi
def turnOffMotors(): #creates object to quit all motors
	mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

#atexit.register(turnOffMotors) # makes sure if exits to stop all motors instantly


pi = pigpio.pi();
global flag1
flag1 = 0

#sets the motors to names
base = mh.getMotor(3)
joint = mh.getMotor(2)
elbow = mh.getMotor(4)
pinch = mh.getMotor(1)

#set speeds for all motors- 150 medium speed, range 0-255
base.setSpeed(150)
joint.setSpeed(150)
elbow.setSpeed(150)
pinch.setSpeed(150)


try:
        while True:
                inp = client.recv(1024)
                print inp

                if (inp == "Right Rotation"):
                        print("Rotating Arm to the Right")
                        base.run(Adafruit_MotorHAT.BACKWARD)
                        time.sleep(2)
                        turnOffMotors()      
            
                elif (inp == "Left Rotation"):
                        print("Rotating Arm to the Left")
                        base.run(Adafruit_MotorHAT.FORWARD)
                        time.sleep(2)
                        turnOffMotors()
                
                elif (inp == "Arm Up"):
                        print("Arm Raising Up")
                        joint.run(Adafruit_MotorHAT.BACKWARD)
                        time.sleep(2)
                        turnOffMotors()
                
                elif (inp == "Arm Down"):
                        print("Arm Lowering Down")
                        joint.run(Adafruit_MotorHAT.FORWARD)
                        time.sleep(2)
                        turnOffMotors()
                
                elif (inp == "Bend Down"):
                        print("Elbow Bending Down")
                        elbow.run(Adafruit_MotorHAT.BACKWARD)
                        time.sleep(2)
                        turnOffMotors()
                
                elif (inp == "Bend Up"):
                        print("Elbow Bending Up")
                        elbow.run(Adafruit_MotorHAT.FORWARD)
                        time.sleep(2)
                        turnOffMotors()
                
                elif (inp == "Grip" and flag1==0):
                        print("Gripping")
                        pinch.run(Adafruit_MotorHAT.FORWARD)
                        time.sleep(.5)
                        turnOffMotors()
                        flag1 = 1

                elif (inp == "Ungrip" and flag1==1):
                        print("Un-Gripping")
                        pinch.run(Adafruit_MotorHAT.BACKWARD)
                        time.sleep(.5)
                        turnOffMotors()
                        flag1 = 0


                else: 
                        pass
                

except KeyboardInterrupt: #will keep going until stopped by user on keyboard
    p.stop() #stop the duty cycle

    GPIO.cleanup() #ending loop
