#!/usr/bin/env python

import rospy
import numpy as np
from datastreaming.msg import ChannelData, Plotarray
from matplotlib import pyplot as plt
import time
import random
import sys
import pylab as pl
import csv
from scipy import signal
from std_msgs.msg import String


class playback():
    def __init__(self):
        
        # set path to datasets
        savetag='_exp2'
        datapath = '/home/jingyan/Documents/ME499-WinterProject/mindwave/src/motor_cortex_ml/data/'
        # csvname =datapath + 'record'+savetag+'.csv'
        csvname =datapath +'record_20rfft.csv'
        data = np.loadtxt(csvname,delimiter = ',')
        
        # get input/output pairs
        self.x = data[:,:-1]
        self.y = data[:,-1]

        self.fs=250 #record frequency for Cyton board
        self.frame=1250 #once the data matrix is N times this number, process DSP
        self.channelnum=8 #using 8 channel Cyton biosensing board
        self.raw_data=[]
        self.filtered_data=[]
        self.average_amp=np.zeros(self.channelnum).reshape(1,self.channelnum)
        self.buff=2500  #number of data store in raw_data matrix
        
        self.band=(16,24) #desired bandpass boundary
        self.notch_val=60 #notch 60 for NA area
        
        self.data_publisher_fdomain=rospy.Publisher('/mindcontrol/average_amp',ChannelData,queue_size=20)
        self.data_publisher_tdomain=rospy.Publisher('/mindcontrol/filtered_data',ChannelData,queue_size=20)
        self.analysis_time=0
        self.average_amp_sample=ChannelData()
        self.realtime_rawdata=ChannelData()
    
    def play(self):
        r=rospy.Rate(50)#(335)
        for i in range(len(self.x)):
            self.non_filter(self.x[i])
            # self.filter_fft(self.x[i])
            # self.data_publisher_tdomain.publish(str(self.x[i]))
            r.sleep()
            # rospy.sleep(0.002)
            if rospy.is_shutdown():
                break       
        

        
    def filter_fft(self,sample):
          
        if len(self.raw_data)>=self.frame and len(self.raw_data) %5==0:
            if self.analysis_time==0: print('=======frame initialized, start to analysis========')
        # if len(self.raw_data)!= 0 and len(self.raw_data) %self.frame ==0:
            self.raw_data=self.raw_data[-self.frame:]
            
            _average_amp=[]
            ##Store buff number of data in the matrix for DSP
            channel_extract=np.array(self.raw_data)
            for k in range(self.channelnum):
                
                channel_data=channel_extract[:,k]
                # channel_filtered=self.bandpass(self.band[0],self.band[1],channel_data,self.fs)
                self.freq,self.y=self.fft(channel_data,self.fs)##FFT for particular channel##
                #average and log1p amp of desired frequency
                freq_ind=np.where((self.freq>=self.band[0])&(self.freq<=self.band[1]))[0] #take diresed frequency
                self.desired_freq=self.freq[freq_ind]
                self.amp_of_desired_freq=self.y[freq_ind]
                    
                average_amp_desired=np.mean(self.amp_of_desired_freq)
                # print(average_amp_desired)
                setattr(self.average_amp_sample,"channel"+str(k+1),average_amp_desired)

            self.data_publisher_fdomain.publish(self.average_amp_sample) #!!! average amp at given frequency range
            self.analysis_time=self.analysis_time+1
            
        self.raw_data.append(sample)

    def non_filter(self,sample):
        
        data=sample
        for k in range(self.channelnum):
            setattr(self.realtime_rawdata,"channel"+str(k+1),data[k])
        self.data_publisher_fdomain.publish(self.realtime_rawdata) 
  
  
        
    def bandpass(self,start,stop,data,fs):
        bp_Hz = np.array([start, stop])
        b, a = signal.butter(5, bp_Hz / (fs / 2.0), btype='bandpass')
        return signal.lfilter(b, a, data, axis=0)

    def notch(self,val, data, fs):
        bp_stop_Hz = val + 3.0 * np.array([-1, 1])
        b, a = signal.butter(3, bp_stop_Hz / (fs / 2.0), 'bandstop')
        return signal.lfilter(b, a, data)
    
    def fft(self,data, fs):
        L = len(data)
        freq = np.linspace(0.0, 1.0 / (2.0 * fs **-1), int(L / 2))
        yi = np.fft.fft(data)#[1:]
        y = yi[range(int(L / 2))]
        # ysample= (2.0*abs(yi/L))[range(int(L/2))]
        return freq, abs(y)


def main():
    rospy.init_node("data_playingback",anonymous=True)
    
    try:
       
        pb=playback()
        pb.play()
        print 'Has analyzed data ',pb.analysis_time,'times'
        
        
    except rospy.ROSInterruptException: pass

    rospy.spin()
    
if __name__ == '__main__':
	main()