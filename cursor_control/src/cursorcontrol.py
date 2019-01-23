#!/usr/bin/env python
import os
import rospy
from std_msgs.msg import String
import numpy as np

class motor_imagine():

    def __init__(self):
        
        self.sample_data_sub=rospy.Subscriber('/mindcontrol/channel_data',String,self.ml_model)

        self.cursor_command=1

        if self.cursor_command == 1:
            #move left
            os.system("xdotool mousemove_relative -- -1 0")
        elif self.cursor_command == 2:
            #move right
            os.system("xdotool mousemove_relative 1 0")
        elif self.cursor_command ==3:
            #move up
            os.system("xdotool mousemove_relative -- 0 -1")
        elif self.cursor_command==4:
            #move down
            os.system("xdotool mousemove_relative 0 1")
        else:
            pass            

    def ml_model(self,data):
        #self.cursor_command=argmax()...
        self.cursor_command=1
        


def main():
    rospy.init_node('motor_imagine',anonymous=True)

    while not rospy.is_shutdown():
        try:
            motor=motor_imagine()
        except rospy.ROSInterruptException: pass
        

    
if __name__ == '__main__':
	main()