#!/usr/bin/env python
import os
import rospy
from std_msgs.msg import String
import numpy as np
from std_msgs.msg import Int32

class motor_imagine:

    def __init__(self):
        
        self.debounce_array=[]
        self.sample_data_sub=rospy.Subscriber('/mindcontrol/mouse_command',Int32,self.command_sign)
        
    def command_sign(self,data):
        self.cursor_command=data.data
        self.debounce_array.append(self.cursor_command)
        if len(self.debounce_array)>=2:
            self.debounce_array=self.debounce_array[-2:]
            print(self.cursor_command)
            if self.debounce_array[0]==self.debounce_array[1]:
                self.move_mouse(self.debounce_array[0])
        
    def move_mouse(self,com):
        # self.cursor_command=1
        
        if com == 1:
            #move left
            os.system("xdotool mousemove_relative -- -1 0")
        elif com == 2:
            #move right
            os.system("xdotool mousemove_relative 1 0")
        # elif self.cursor_command ==3:
        #     #move up
        #     os.system("xdotool mousemove_relative -- 0 -1")
        # elif self.cursor_command==4:
            #move down
            # os.system("xdotool mousemove_relative 0 1")
        # elif self.cursor_command== 0: pass
            # print('holding')  

        # self.rate=rospy.Rate(50)  
        # self.rate.sleep()   

def main():
    rospy.init_node('motor_imagine',anonymous=True)

    
    try:
        
        motor=motor_imagine()
            
        
    except rospy.ROSInterruptException:pass
        

    rospy.spin()
if __name__ == '__main__':
	main()