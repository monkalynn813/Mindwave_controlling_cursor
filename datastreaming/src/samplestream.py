#!/usr/bin/env python

from openbci.cyton import OpenBCICyton
import rospy
import numpy as np
from std_msgs.msg import String
import ref_streaming as waves
from scipy import signal



# port='/dev/ttyUSB0'
# eeg=OpenBCICyton()


class datastreaming:
    def __init__(self):

        self.eeg=OpenBCICyton() #Openbci_python class for cyton board
        rospy.sleep(1.0)

        self.fs=250 #record frequency for Cyton board
        self.frame=250 #once the data matrix is N times this number, process DSP
        self.raw_data=[]
        self.filtered_data=[]
        self.buff=2500  #number of data store in raw_data matrix
        self.channelnum=8 #using 8 channel Cyton biosensing board
       
        
        self.band=(8,13) #desired bandpass boundary
        

        self.br=waves.Brain_waves(self.eeg,8,self.fs)
        self.data_publisher=rospy.Publisher('/mindcontrol/channel_data',String,queue_size=20)

    def filter(self,sample):
        if len(self.raw_data)!= 0 and len(self.raw_data) %self.frame ==0:
            self.raw_data=self.raw_data[-self.buff:]
            channel_extract=np.array(self.raw_data)
            for k in range(self.channelnum)

            # filtered_sample= ######
                        
            # self.filtered_data.append(filtered_sample)
            
        self.raw_data.append(sample.channel_data)

        # print(sample.channel_data)
        # filtered_sample=str(filtered_sample)
        # self.data_publisher.publish(filtered_sample)

        #channel_data=sample.channel_data
        #publish topic here
    def bandpass(self,start,stop,data,fs):
        bp_Hz = np.array([start, stop])
        b, a = signal.butter(5, bp_Hz / (fs / 2.0), btype='bandpass')
        return signal.lfilter(b, a, data, axis=0)

    def notch(self,val, data, fs):
        bp_stop_Hz = val + 3.0 * np.array([-1, 1])
        b, a = signal.butter(3, bp_stop_Hz / (fs / 2.0), 'bandstop')
        fin = signal.lfilter(b, a, data)
        return fin

    def stream(self):
        self.eeg.start_streaming(self.filter,5)
        print(len(self.raw_data))
        testform=np.array(self.raw_data)
        print(testform[:,1].shape)
        
        
        
        # self.br.start_streaming(self.filter,self.band,25,file_name='data/test.csv')
        

def main():
    rospy.init_node('data_streaming',anonymous=True)
    stream=datastreaming()
    

    try:
        stream.stream()
    except rospy.ROSInterruptException: pass
       
    

if __name__ == '__main__':
    main()