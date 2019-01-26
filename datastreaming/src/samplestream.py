#!/usr/bin/env python

from openbci.cyton import OpenBCICyton
import rospy
import numpy as np
from std_msgs.msg import String
import ref_streaming as waves



port='/dev/ttyUSB0'
eeg=OpenBCICyton()

class datastreaming:
    def __init__(self):

        self.eeg=eeg
        self.data_publisher=rospy.Publisher('/mindcontrol/channel_data',String,queue_size=20)
        rospy.sleep(1.0)
        
        self.band=(10,30)
        self.notch=60

    
        

    def filter(self,sample):
        # print(sample.channel_data)
        self.filtered_sample=str(sample.channel_data)
        self.data_publisher.publish(self.filtered_sample)
        #channel_data=sample.channel_data
        #publish topic here
        

def main():
    rospy.init_node('data_streaming',anonymous=True)
    stream=datastreaming()

    try:
        while not rospy.is_shutdown():
            eeg.start_streaming(stream.filter)
    except rospy.ROSInterruptException: pass
       
    

if __name__ == '__main__':
    main()