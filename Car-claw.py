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
port = 1234
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


ESC=4  #Connect the ESC in this GPIO pin 

pi = pigpio.pi();
pi.set_servo_pulsewidth(ESC, 0) 

max_value = 2000 #change this if your ESC's max value is different or leave it be
min_value = 700  #change this if your ESC's min value is different or leave it be

GPIO.setmode(GPIO.BOARD) #gives the setup for GPIO on the RPi boad

GPIO.setup(11,GPIO.OUT) #says that pin 11 which is connected to the servo2 is an output for the code

b = GPIO.PWM(11,50) #pin 11 controls second servo PWM at 50HZ
b.start(7.5) #starting for 2nd pin as well


try:
    print "I'm Starting the motor, I hope its calibrated and armed, if not restart by giving 'x'"
    time.sleep(1)
    speed = 1500    # change your speed if you want to.... it should be between 700 - 2000
    while True:
        pi.set_servo_pulsewidth(ESC, speed)
        inp = client.recv(1024)
        print inp
            
        if inp == "Forward":
            b.ChangeDutyCycle(7.5) #servo straight
            speed = 1580    # motor goes forward
            print ("going forwards straight")

        elif inp == "Forward-Left":
            print("Left going forwards")
            b.ChangeDutyCycle(6) #left on servo2
            speed = 1580    # motor goes forward

        elif inp == "Forward-Right":
            print("Right going forwards")
            b.ChangeDutyCycle(9) #right on servo2
            speed = 1580    # motor goes forward
            
        elif inp == "Backward":    
            b.ChangeDutyCycle(7.5) #neutral on servo2
            speed = 1430    # motor goes backwards
            print ("going backwards straight")
            

        elif inp == "Backward-Right":
            b.ChangeDutyCycle(9) #right on servo 2
            speed = 1430 #motor goes backwards
            print ("going backwards right")
            
        elif inp == "Backward-Left":
            b.ChangeDutyCycle(6) #right on servo 2
            speed = 1430 #motor goes backwards
            print ("going backwards left")
            

        elif inp == "Stop":
            b.ChangeDutyCycle(7.5) #neutral on servo2
            speed = 1500   #dont move
            print ("stopped")



except KeyboardInterrupt: #will keep going until stopped by user on keyboard
    p.stop() #stop the duty cycle

    GPIO.cleanup() #ending loop
