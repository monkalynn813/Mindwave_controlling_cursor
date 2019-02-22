#!/usr/bin/env python

from openbci.cyton import OpenBCICyton
import rospy
import numpy as np
from scipy import signal
from matplotlib import pyplot as plt
from datastreaming.msg import ChannelData, Plotarray
from math import log1p


class datastreaming:
    def __init__(self):
        
        # self.port='/dev/ttyUSB0'
        self.eeg=OpenBCICyton() #Openbci_python class for cyton board
        rospy.sleep(1.0)

        self.fs=250 #record frequency for Cyton board
        self.frame=750 #once the data matrix is N times this number, process DSP
        self.channelnum=8 #using 8 channel Cyton biosensing board
        self.raw_data=[]
        self.filtered_data=[]
                
        self.band=(16,24) #desired bandpass boundary
        self.notch_val=60 #notch 60 for NA area
        self.mode=rospy.get_param("~mode",'fft')

        #########data sampling################
        self.data_publisher_tdomain=rospy.Publisher('/mindcontrol/filtered_data',ChannelData,queue_size=20)
        self.data_publisher_fdomain=rospy.Publisher('/mindcontrol/average_amp',ChannelData,queue_size=20)
        self.analysis_time=0
        self.average_amp_sample=ChannelData()
        self.realtime_bpdata=ChannelData()
        self.realtime_rawdata=ChannelData()

        #########plotting####################
        self.ampplot=Plotarray()
        self.freqplot=Plotarray()
        self.fft_publisher=rospy.Publisher('/mindcontrol/fft',Plotarray,queue_size=20)
        self.freq_publisher=rospy.Publisher('/mindcontrol/freq',Plotarray,queue_size=20)
        
    def filter_fft(self,sample):
          
        if len(self.raw_data)>=self.frame and len(self.raw_data) %10==0:
            if self.analysis_time==0: print('=======frame initialized, start to analysis========')
        # if len(self.raw_data)!= 0 and len(self.raw_data) %self.frame ==0:
            self.raw_data=self.raw_data[-self.frame:]
            
            _average_amp=[]
            ##Store buff number of data in the matrix for DSP
            channel_extract=np.array(self.raw_data)
            for k in range(self.channelnum):
                
                channel_data=channel_extract[:,k]
                
                self.freq,self.y=self.fft(channel_data,self.fs)##FFT for particular channel##
                #average and log1p amp of desired frequency
                freq_ind=np.where((self.freq>=self.band[0])&(self.freq<=self.band[1]))[0] #take diresed frequency
                self.desired_freq=self.freq[freq_ind]
                self.amp_of_desired_freq=self.y[freq_ind]
                    
                average_amp_desired=np.mean(self.amp_of_desired_freq)
                # print(average_amp_desired)
                setattr(self.average_amp_sample,"channel"+str(k+1),average_amp_desired)
                setattr(self.ampplot,"channel"+str(k+1),np.ndarray.tolist(self.amp_of_desired_freq)) #for plotting , comment when not plotting
                # _average_amp.append(average_amp_desired)   #put all channel's average amp for particular frequency in matrix             


            self.freqplot.channel1=np.ndarray.tolist(self.desired_freq) #plot

            self.fft_publisher.publish(self.ampplot) #plot
            self.freq_publisher.publish(self.freqplot) #plot
            self.data_publisher_fdomain.publish(self.average_amp_sample) #!!! average amp at given frequency range
            self.analysis_time=self.analysis_time+1

        self.raw_data.append(sample.channel_data)
        if rospy.is_shutdown():
            self.eeg.stop()
    def filter_bp(self,sample):
                 
        if len(self.raw_data)>=self.frame and len(self.raw_data) %5==0:
            
            if self.analysis_time==0: print('=======frame initialized, start to analysis========')
        # if len(self.raw_data)!= 0 and len(self.raw_data) %self.frame ==0:
            self.raw_data=self.raw_data[-self.frame:]
            
            ##Store buff number of data in the matrix for DSP
            channel_extract=np.array(self.raw_data)
            for k in range(self.channelnum):
                
                channel_data=channel_extract[:,k]
                
                channel_filtered=self.bandpass(self.band[0],self.band[1],channel_data,self.fs) #only pass the bandpass filter
                # channel_filtered=self.notch(self.notch_val,channel_bp,self.fs)#pass bandpass filtered data through notch filter
                
                #put filtered data in (datanum * channelnum) matrix
                # channel_filtered=channel_filtered.reshape(len(channel_filtered),1) 
                setattr(self.realtime_bpdata,"channel"+str(k+1),channel_filtered[-1])

            #     if k==0:
            #         self.filtered_data=channel_filtered
            #     else:
            #         self.filtered_data=np.append(self.filtered_data,channel_filtered,axis=1) #alwasy store the latest filtered data (past 2500 gourps of data)
                            
            # filtered_sample = self.filtered_data[-1] 
            
            self.data_publisher_tdomain.publish(self.realtime_bpdata)
            self.analysis_time=self.analysis_time+1
        self.raw_data.append(sample.channel_data)
        if rospy.is_shutdown():
            self.eeg.stop()
    def non_filter(self,sample):
        
        data=sample.channel_data
        for k in range(self.channelnum):
            setattr(self.realtime_rawdata,"channel"+str(k+1),data[k])
        self.data_publisher_tdomain.publish(self.realtime_rawdata) 
        if rospy.is_shutdown():
            self.eeg.stop()     

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


    def stream(self):
        if self.mode=='fft':
            rospy.loginfo("=====control mode=====")
            callback=self.filter_fft
        elif self.mode=='record':
            rospy.loginfo("=====record mode======")
            callback=self.non_filter
        elif self.mode=='bandpass':
            callback=self.filter_bp

        self.eeg.start_streaming(callback)
        print 'Has analyzed data ',self.analysis_time,'times'
        

def main():
    rospy.init_node('data_streaming',anonymous=True)
    stream=datastreaming()
    

    try:
        stream.stream()
    except rospy.ROSInterruptException: pass
       
    

if __name__ == '__main__':
    main()