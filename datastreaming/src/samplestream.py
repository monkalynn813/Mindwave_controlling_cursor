#!/usr/bin/env python

from openbci.cyton import OpenBCICyton
import rospy
import numpy as np
from std_msgs.msg import String
import ref_streaming as waves
import utils



# port='/dev/ttyUSB0'
# eeg=OpenBCICyton()


class datastreaming:
    def __init__(self):

        self.eeg=OpenBCICyton()
        rospy.sleep(1.0)

        self.fs=250
        self.frame=250
        self.raw_data=[]
        self.filtered_data=[]
        self.buff=2500 
       
        #data sampled at 250Hz for Cyton board
        self.band=(8,13)
        self.notch=60

        self.br=waves.Brain_waves(self.eeg,8,self.fs)
        self.data_publisher=rospy.Publisher('/mindcontrol/channel_data',String,queue_size=20)

    def filter(self,sample):
        if len(self.raw_data)!= 0 and len(self.raw_data) %self.frame ==0:
            self.raw_data=self.raw_data[-self.buff:]

            filtered_sample=waves.Brain_waves.analyze(self.raw_data,self.band[0]) ######
            self.filtered_data.append(filtered_sample)
            
        self.raw_data.append(sample.channel_data)

        # print(sample.channel_data)
        filtered_sample=str(filtered_sample)
        self.data_publisher.publish(filtered_sample)

        #channel_data=sample.channel_data
        #publish topic here
    def stream(self):
        self.eeg.start_streaming(self.filter,25)
        
        # self.br.start_streaming(self.filter,self.band,25,file_name='data/test.csv')
        

def main():
    rospy.init_node('data_streaming',anonymous=True)
    stream=datastreaming()
    

    try:
        stream.stream()
    except rospy.ROSInterruptException: pass
       
    

if __name__ == '__main__':
    main()