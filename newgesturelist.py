import Leap, sys, thread, time, math
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import socket

client = socket.socket()
client2 = socket.socket()
#defines client socket
client.connect(('192.168.11.3', 1234))
client2.connect(('192.168.11.3', 5678))
#connection to the server/pi with address in pi code


while True:
#keeps loop running
    class leapsListener(Leap.Listener):
        finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']

        def on_connect(self, controller):
            controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
            controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
            controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
            controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);
            #enables all gestures

        def on_frame(self, controller):
            frame = controller.frame()           
            #capture data from the frame

            for hand in frame.hands:

                hand_dir = hand.direction # go to this link... https://developer.leapmotion.com/documentation/python/api/Leap.Hand.html#Leap.Hand.direction
                ang = hand_dir.pitch # go to thi link... https://developer.leapmotion.com/documentation/python/api/Leap.Vector.html#Leap.Vector.pitch
                ang_yaw = hand_dir.yaw # go to this link... https://developer.leapmotion.com/documentation/python/api/Leap.Vector.html#Leap.Vector.yaw           
                if hand.is_left:
                   handType = "Left hand" 
                elif hand.is_right:
                   handType = "Right hand"
                   
                #determines which hand is detected

                if(handType == "Left hand"):
                    finger = frame.fingers.extended()
                    finger_count = len(frame.fingers.extended())
                    if finger_count == 2:
                        print "2 fingers detected-gripping"
                        client2.send("Grip")
                        
                    elif finger_count == 3:
                        print "3 fingers detected- ungripping"
                        client2.send("Ungrip")
                                     
                    else:
                        pass
                
                #makes sure only reads left hand
                    for gesture in frame.gestures():

                        if gesture.type == Leap.Gesture.TYPE_SWIPE:
                            swipe = SwipeGesture(gesture)
                            swipeDir = swipe.direction
                            pinch = hand.pinch_strength
                            
                            #defines what to use for swipe and swipeDir
                            #0 open, 1 closed
                            #if more than .5 then closed
                            if(pinch > .5):
                                print ("Close Gripper")
                                client2.send("Grip")
##                            elif(pinch < .5):
##                                print ("Open Griper")
##                                client2.send("Ungrip")
                            if(swipeDir.x>0 and math.fabs(swipeDir.x) > math.fabs(swipeDir.y) and math.fabs(swipeDir.z) < math.fabs(swipeDir.x)):
                                print ("Right Rotation")
                                client2.send("Right Rotation")
                            elif(swipeDir.x<0 and math.fabs(swipeDir.x) > math.fabs(swipeDir.y) and math.fabs(swipeDir.z) < math.fabs(swipeDir.x)):
                                print ("Left Rotation")
                                client2.send("Left Rotation")
                            elif(swipeDir.y>0 and math.fabs(swipeDir.x) < math.fabs(swipeDir.y) and math.fabs(swipeDir.z) < math.fabs(swipeDir.y)):
                                print ("Arm Up")
                                client2.send("Arm Up")
                            elif(swipeDir.y<0 and math.fabs(swipeDir.x) < math.fabs(swipeDir.y) and math.fabs(swipeDir.z) < math.fabs(swipeDir.y)):
                                print ("Arm Down")
                                client2.send("Arm Down")
                            elif(swipeDir.z>0 and math.fabs(swipeDir.z) > math.fabs(swipeDir.y) and math.fabs(swipeDir.z) > math.fabs(swipeDir.x)):
                                print ("Bend Down")
                                client2.send("Bend Down")
                            elif(swipeDir.z<0 and math.fabs(swipeDir.z) > math.fabs(swipeDir.y) and math.fabs(swipeDir.z) > math.fabs(swipeDir.x)):
                                print ("Bend Up")
                                client2.send("Bend Up")
                            #math.fabs() is for absolute value, and have to make sure the direction
                            #for one is greater than other so it knows for sure rihgt or left
                            #x is left and right, y is up and down, z is backwards and forwards

                if(handType == "Right hand"):
                    if(ang <= -0.25):
                        if(ang_yaw>=0.20):
                                print "forward-Right"
                                client.send("Forward-Right")

                        elif(ang_yaw<=-0.20):
                                print "Forward-Left"
                                client.send("Forward-Left")

                        else:
                                print "Forward"
                                client.send("Forward")
                                

                    elif(ang >= 0.25):
                        if(ang_yaw>=0.30):
                                print "Backward-Right"
                                client.send("Backward-Right")

                        elif(ang_yaw<=-0.50):
                                print "Backward-Left"
                                client.send("Backward-Left")

                        else:
                                print "Backward"
                                client.send("Backward")

                    else:
                        print "Stop"
                        client.send("Stop")


        def state_string(self, state):
            if state == Leap.Gesture.STATE_START:
                return "STATE_START"

            if state == Leap.Gesture.STATE_UPDATE:
                return "STATE_UPDATE"

            if state == Leap.Gesture.STATE_STOP:
                return "STATE_STOP"

            if state == Leap.Gesture.STATE_INVALID:
                return "STATE_INVALID"

    def main():
        listener = leapsListener()
        controller = Leap.Controller()
        # Creates a listener and controller to pass arguments
        
        controller.add_listener(listener)
        #the controller sends data captured to the listener

        print""
        controller.remove_listener(listener)
        #removes it when done reading data

    if __name__ == "__main__":
        main()
