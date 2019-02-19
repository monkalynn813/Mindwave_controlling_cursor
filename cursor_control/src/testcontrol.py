#!/usr/bin/env python
import os
import rospy
from std_msgs.msg import String
import numpy as np
from std_msgs.msg import Int32

class motor_imagine:

    def __init__(self):
        
        
        self.sample_data_sub=rospy.Subscriber('/mindcontrol/mouse_command',Int32,self.command_sign)
        
    def command_sign(self,data):
        # self.cursor_command=data.data
        print(data)
    
def main():
    rospy.init_node('motor_imagine')

    
    try:
        
        motor=motor_imagine()
            
        
    except rospy.ROSInterruptException:pass
        

    rospy.spin()
if __name__ == '__main__':
	main()