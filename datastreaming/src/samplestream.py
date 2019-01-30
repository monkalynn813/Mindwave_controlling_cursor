#!/usr/bin/env python

from openbci.cyton import OpenBCICyton
import rospy
import numpy as np
from std_msgs.msg import String
import ref_streaming as waves
from scipy import signal




class datastreaming:
    def __init__(self):
        
        # self.port='/dev/ttyUSB0'
        self.eeg=OpenBCICyton() #Openbci_python class for cyton board
        rospy.sleep(1.0)

        self.fs=250 #record frequency for Cyton board
        self.frame=250 #once the data matrix is N times this number, process DSP
        self.raw_data=[]
        self.filtered_data=[]
        self.buff=2500  #number of data store in raw_data matrix
        self.channelnum=8 #using 8 channel Cyton biosensing board
       
        
        self.band=(7,13) #desired bandpass boundary
        self.notch_val=60 #notch 60 for NA area

        self.br=waves.Brain_waves(self.eeg,8,self.fs)
        self.data_publisher=rospy.Publisher('/mindcontrol/channel_data',String,queue_size=20)

    def filter(self,sample):

        if len(self.raw_data)!= 0 and len(self.raw_data) %self.frame ==0:
            self.raw_data=self.raw_data[-self.buff:]
            
            ##Store buff number of data in the matrix for DSP
            channel_extract=np.array(self.raw_data)
            for k in range(self.channelnum):
                channel_data=channel_extract[:,k]
                
                channel_bp=self.bandpass(self.band[0],self.band[1],channel_data,self.fs) #only pass the bandpass filter
                channel_filtered=self.notch(self.notch_val,channel_bp,self.fs)#pass bandpass filtered data through notch filter
                #put filtered data in (datanum * channelnum) matrix
                channel_filtered=channel_filtered.reshape(len(channel_filtered),1) 

                if k==0:
                    self.filtered_data=channel_filtered
                else:
                    self.filtered_data=np.append(self.filtered_data,channel_filtered,axis=1) #alwasy store the latest filtered data (past 2500 gourps of data)
            
            filtered_sample = self.filtered_data[-1]
            filtered_sample=str(filtered_sample)
            self.data_publisher.publish(filtered_sample)
            
        
        self.raw_data.append(sample.channel_data)

    def bandpass(self,start,stop,data,fs):
        bp_Hz = np.array([start, stop])
        b, a = signal.butter(5, bp_Hz / (fs / 2.0), btype='bandpass')
        return signal.lfilter(b, a, data, axis=0)

    def notch(self,val, data, fs):
        bp_stop_Hz = val + 3.0 * np.array([-1, 1])
        b, a = signal.butter(3, bp_stop_Hz / (fs / 2.0), 'bandstop')
        fin = signal.lfilter(b, a, data)
        return fin
    
    def fft(self,data, fs):
        L = len(data)
        freq = np.linspace(0.0, 1.0 / (2.0 * fs **-1), int(L / 2))
        yi = np.fft.fft(data)#[1:]
        y = yi[range(int(L / 2))]
        return freq, abs(y)


    def stream(self):
        self.eeg.start_streaming(self.filter,5)
        
        print(np.array(self.raw_data).shape)
        print(self.filtered_data.shape)
        
        
        # self.br.start_streaming(self.filter,self.band,25,file_name='data/test.csv')
        

def main():
    rospy.init_node('data_streaming',anonymous=True)
    stream=datastreaming()
    

    try:
        stream.stream()
    except rospy.ROSInterruptException: pass
       
    

if __name__ == '__main__':
    main()