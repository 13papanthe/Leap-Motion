from AMSpi import AMSpi
import os     #importing os library so as to communicate with the system
import time   #importing time library to make Rpi wait because its too impatient 
os.system ("sudo pigpiod") #Launching GPIO library
time.sleep(1) # As i said it is too impatient and so if this delay is removed you will get an error
import pigpio #importing GPIO library
import socket
import RPi.GPIO as GPIO #importing GPIO code for the pi

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sets up the server with socket and calling the socket libraries

ip = '10.159.109.42'
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

pi = pigpio.pi();
global flag1
flag1 = 0

try:
       while True:
        inp = client.recv(1024)
        print inp
        

        
        with AMSpi() as amspi:
            # Set PINs for controlling shift register (GPIO numbering)
            amspi.set_74HC595_pins(40, 38, 36)
            # Set PINs for controlling all 4 motors (GPIO numbering)
            amspi.set_L293D_pins(29, 31, 33, 35)
            amspi.stop_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4])

            if (inp == "Right Rotation"):
                print("Rotating Arm to the Right")
                amspi.run_dc_motors([amspi.DC_Motor_1], clockwise=False)
                time.sleep(2)
                amspi.stop_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4])
            
            elif (inp == "Left Rotation"):
                print("Rotating Arm to the Left")
                amspi.run_dc_motors([amspi.DC_Motor_1])
                time.sleep(2)
                amspi.stop_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4])
                
            elif (inp == "Arm Up"):
                print("Arm Raising Up")
                amspi.run_dc_motors([amspi.DC_Motor_2])
                time.sleep(1.5)
                amspi.stop_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4])

            elif (inp == "Arm Down"):
                print("Arm Lowering Down")
                amspi.run_dc_motors([amspi.DC_Motor_2], clockwise=False)
                time.sleep(1)
                amspi.stop_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4])

            elif (inp == "Bend Down"):
                print("Elbow Bending Down")
                amspi.run_dc_motors([amspi.DC_Motor_4])
                time.sleep(2)
                amspi.stop_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4])

            elif (inp == "Bend Up"):
                print("Elbow Bending Up")
                amspi.run_dc_motors([amspi.DC_Motor_4], clockwise=False)
                time.sleep(2)
                amspi.stop_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4])

            elif (inp == "Grip" and flag1==0):
                print("Gripping")
                amspi.run_dc_motors([amspi.DC_Motor_3])
                time.sleep(.5)
                amspi.stop_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4])
                flag1 = 1

            elif (inp == "Ungrip" and flag1==1):
                print("Un-Gripping")
                amspi.run_dc_motors([amspi.DC_Motor_3], clockwise=False)
                time.sleep(.5)
                amspi.stop_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4])
                flag1 = 0


            else: 
                pass

except KeyboardInterrupt: #will keep going until stopped by user on keyboard
    p.stop() #stop the duty cycle

    GPIO.cleanup() #ending loop
