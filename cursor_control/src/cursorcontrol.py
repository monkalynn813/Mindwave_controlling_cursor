#!/usr/bin/env python
import os
import rospy
from std_msgs.msg import String
import numpy as np
from std_msgs.msgi import Int32

class motor_imagine:

    def __init__(self):
        
        
        self.sample_data_sub=rospy.Subscriber('/mindcontrol/mouce_command',Int32,self.command_sign)

        self.cursor_command=1

        if self.cursor_command == -1:
            #move left
            os.system("xdotool mousemove_relative -- -1 0")
        elif self.cursor_command == 1:
            #move right
            os.system("xdotool mousemove_relative 1 0")
        elif self.cursor_command ==3:
            #move up
            os.system("xdotool mousemove_relative -- 0 -1")
        elif self.cursor_command==4:
            #move down
            os.system("xdotool mousemove_relative 0 1")
        elif self.cursor_command== 0:
            pass  

        self.rate=rospy.Rate(50)  
        self.rate.sleep()        
        
    def command_sign(self,data):
        self.cursor_command=data.data
        


def main():
    rospy.init_node('motor_imagine',anonymous=True)

    
    try:
        while not rospy.is_shutdown():
            motor=motor_imagine()
            
        
    except rospy.ROSInterruptException:pass
        

    
if __name__ == '__main__':
	main()