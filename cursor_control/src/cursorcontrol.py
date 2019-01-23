#!/usr/bin/env python
import os
import rospy
from std_msgs.msg import String
import numpy as np

class motor_imagine():

    def __init__(self):
        
        self.sample_data_sub=rospy.Subsriber('/mindcontrol/channel_data',String,self.ml_model)
        self.cursor_pub=rospy.Pulisher('/mindcontrol/cursorcommand',String)
        os.system("xdotool mousemove_relative 10 0")

    def ml_model(self,data):
        pass
        

def main():
    rospy.init_node('motor_imagine',anonymous=True)
    try:
        motor=motor_imagine()
    except rospy.ROSInterruptException: pass

    
if __name__ == '__main__':
	main()