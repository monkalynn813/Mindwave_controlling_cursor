#!/usr/bin/env python

from openbci.cyton import OpenBCICyton
import rospy
import numpy as np
from std_msgs.msg import String


eeg=OpenBCICyton()
class datastreaming():
    def __init__(self):

        self.eeg=eeg
        self.data_publisher=rospy.Publisher('/mindcontrol/channel_data',String,queue_size=20)
        rospy.sleep(2.0)

    def filter(self,sample):
        print(sample)
        publishstringsample=str(sample)
        self.data_publisher(publishstringsample)
        #channel_data=sample.channel_data
        #publish topic here
        

def main():
    rospy.init_node('data_streaming',anonymous=True)
    try:
        stream=datastreaming()
        eeg.start_streaming(stream.filter)
    except rospy.ROSInterruptException: pass    

if __name__ == '__main__':
    main()