#!/usr/bin/env python

import rospy
import numpy as np
from datastreaming.msg import ChannelData, Plotarray
import time
import random
import sys
import datetime
import os
import cv2, cv_bridge
from sensor_msgs.msg import Image

class recorder():
    def __init__(self):
        savetag='_exp19_record_gui'
        self.savedir="/home/jingyan/Documents/ME499-WinterProject/mindwave/src/motor_cortex_ml/data/"
        self.savepath=self.savedir+'record'+savetag+'.csv'
        self.delim = ','
        self.fs=50
        self.recordsize=1 #number of trails for each task
        self.detailsize=7.5*self.fs # number of sample in each trail
        self.baseline_cross_time=6*self.fs  #time of showing cross in baseline trail
        ######parameter for each left/right trail
        self.intrail_cross_time=2*self.fs 
        self.intrail_cue_time=1.5*self.fs
        self.intrail_holdmi_time=2.5*self.fs
        self.intrail_break_time=1.5 *self.fs
        self.detailcounter=0  #counter for counting number of samples recorded in each left/right trail
        self.beepfreq=1000  #1kHZ
        self.beepduration=0.07  #70ms

        self.leftcounter=0
        self.rightcounter=0
        self.centercounter=0
        self.restcounter=0
        #####GUI
        ##read image and store ahead##
        self.crossimg=cv2.imread('/home/jingyan/Documents/ME499-WinterProject/mindwave/src/image/cross.png')
        self.leftimg=cv2.imread('/home/jingyan/Documents/ME499-WinterProject/mindwave/src/image/left.png')
        self.rightimg=cv2.imread('/home/jingyan/Documents/ME499-WinterProject/mindwave/src/image/right.png')
        self.restimg=cv2.imread('/home/jingyan/Documents/ME499-WinterProject/mindwave/src/image/rest.png')
        self.image_pub=rospy.Publisher("/mindcontrol/GUI_image",Image,queue_size=10)
        self.bridge=cv_bridge.CvBridge()
        
        # self.fftamp_subscriber=rospy.Subscriber('/mindcontrol/filtered_data',ChannelData,self.fftcallback)
        # self.fftamp_subscriber=rospy.Subscriber('/mindcontrol/average_amp2',ChannelData,self.secondfftcallback)
        self.fftamp_subscriber=rospy.Subscriber('/mindcontrol/average_amp',ChannelData,self.fftcallback)
    
    def fftcallback(self,data):
        
        self.fftamp1=data.channel1
        self.fftamp2=data.channel2
        self.fftamp3=data.channel3
        self.fftamp4=data.channel4
        self.fftamp5=data.channel5
        self.fftamp6=data.channel6
        self.fftamp7=data.channel7
        self.fftamp8=data.channel8
        self.fftamp11=data.channel11
        self.fftamp12=data.channel12
        self.fftamp13=data.channel13
        self.fftamp14=data.channel14
        self.fftamp15=data.channel15
        self.fftamp16=data.channel16
        self.fftamp17=data.channel17
        self.fftamp18=data.channel18
        self.fftamp21=data.channel21
        self.fftamp22=data.channel22
        self.fftamp23=data.channel23
        self.fftamp24=data.channel24
        self.fftamp25=data.channel25
        self.fftamp26=data.channel26
        self.fftamp27=data.channel27
        self.fftamp28=data.channel28        


        if self.centercounter<int(self.recordsize):
            if self.detailcounter<self.detailsize:
                # if self.centercounter==0: os.system("xdotool mousemove 960 880")
                self.focuscenter()
                self.detailcounter+=1
                if self.detailcounter==self.detailsize:
                    self.detailcounter=0
                    self.centercounter+=1
        elif self.detailcounter<self.detailsize:
            if self.detailcounter==0:
                os.system('play -nq -t alsa synth {} sine {}'.format(self.beepduration,self.beepfreq))
                if self.leftcounter<self.recordsize and self.rightcounter<self.recordsize:
                    call_which=random.randint(0,1) #random pick a direction to imagin 0=left; 1=right
                elif self.leftcounter==self.recordsize and self.rightcounter<self.recordsize: call_which=1
                elif self.leftcounter<self.recordsize and self.rightcounter==self.recordsize: call_which=0
                elif self.leftcounter==self.recordsize and self.rightcounter==self.recordsize:
                    raw_input('\n Acquisition finished, press ctrl+c to exit')
                
          
                if call_which==0:
                    self.func=self.focusleft
                    self.leftcounter+=1
                else: 
                    self.func=self.focusright        
                    self.rightcounter+=1  

            
            self.func()
            self.detailcounter+=1
            if self.detailcounter==self.detailsize: self.detailcounter=0  #roll over trail
        
        self.image_pub.publish(self.bridge.cv2_to_imgmsg(self.img,'bgr8'))    
                
    def focuscenter(self):
        if self.detailcounter<self.baseline_cross_time:
            # sys.stdout.write('\r                                ++++++++++++++                           ')
            # sys.stdout.flush()
            self.img=self.crossimg
            if self.detailcounter>=1*self.fs+self.intrail_cross_time: #start to write in file after 0.5s of cue
                label='0'
                self.writeinfile(label)        
        elif self.detailcounter<self.detailsize:
            # sys.stdout.write('\r                                take a break                           ')
            # sys.stdout.flush()  
            self.img=self.restimg
        # label='0'
        # self.writeinfile(label)
        
    def focusleft(self):
        if self.detailcounter<self.intrail_cross_time:
            # sys.stdout.write('\r                                ++++++++++++++                           ')
            # sys.stdout.flush()
            self.img=self.crossimg        
        elif self.detailcounter<self.intrail_cross_time+self.intrail_cue_time:
            # sys.stdout.write('\r        <<<<<<<<<<<<<           ++++++++++++++                           ')
            # sys.stdout.flush()
            self.img=self.leftimg
            if self.detailcounter>=1*self.fs+self.intrail_cross_time: #start to write in file after 0.5s of cue
                label='1'
                self.writeinfile(label)
        elif self.detailcounter<self.intrail_cross_time+self.intrail_cue_time+self.intrail_holdmi_time:
            # sys.stdout.write('\r                                ++++++++++++++                           ')
            # sys.stdout.flush()
            self.img=self.crossimg
            label='1'
            self.writeinfile(label)            
        elif self.detailcounter<self.detailsize:
            # sys.stdout.write('\r                                take a break                           ')
            # sys.stdout.flush()
            self.img=self.restimg

        # label='1'
        # self.writeinfile(label)
        # if self.detailcounter==self.detailsize/2 or self.detailcounter==self.detailsize-10: os.system("xdotool mousemove_relative -- -20 0")
    def focusright(self):
        if self.detailcounter<self.intrail_cross_time:
            # sys.stdout.write('\r                                ++++++++++++++                           ')
            # sys.stdout.flush()
            self.img=self.crossimg        
        elif self.detailcounter<self.intrail_cross_time+self.intrail_cue_time:
            # sys.stdout.write('\r                                ++++++++++++++              >>>>>>>>>>>  ')
            # sys.stdout.flush()
            self.img=self.rightimg
            if self.detailcounter>=1*self.fs+self.intrail_cross_time: #start to write in file after 0.5s of cue
                label='2'
                self.writeinfile(label) 
        elif self.detailcounter<self.intrail_cross_time+self.intrail_cue_time+self.intrail_holdmi_time:
            # sys.stdout.write('\r                                ++++++++++++++                           ')
            # sys.stdout.flush()
            self.img=self.crossimg
            label='2'
            self.writeinfile(label)            
        elif self.detailcounter<self.detailsize: 
            # sys.stdout.write('\r                                take a break                           ')
            # sys.stdout.flush()
            self.img=self.restimg
                
        # label='1'         
        # self.writeinfile(label)
        # if self.detailcounter==self.detailsize/2 or self.detailcounter==self.detailsize-10: os.system("xdotool mousemove_relative 20 0")
    def rest(self):
        sys.stdout.write('\r                                take a break                           ')
        sys.stdout.flush()

    # def writeinfile(self,label):
    #     row=''
    #     row += str(self.fftamp1)
    #     row += self.delim
    #     row += str(self.fftamp2)
    #     row += self.delim
    #     row += str(self.fftamp3)
    #     row += self.delim
    #     row += str(self.fftamp4)
    #     row += self.delim
    #     row += str(self.fftamp5)
    #     row += self.delim
    #     row += str(self.fftamp6)
    #     row += self.delim
    #     row += str(self.fftamp7)
    #     row += self.delim
    #     row += str(self.fftamp8)
    #     row += self.delim
    #     row += str(label)
    #     row += '\n'
    #     with open(self.savepath,'a') as f:
    #         f.write(row)
    def writeinfile(self,label):
        row=''
        row += str(self.fftamp1)
        row += self.delim
        row += str(self.fftamp11)
        row += self.delim
        row += str(self.fftamp21)
        row += self.delim
        row += str(self.fftamp2)
        row += self.delim
        row += str(self.fftamp12)
        row += self.delim
        row += str(self.fftamp22)
        row += self.delim
        row += str(self.fftamp3)
        row += self.delim
        row += str(self.fftamp13)
        row += self.delim
        row += str(self.fftamp23)
        row += self.delim
        row += str(self.fftamp4)
        row += self.delim
        row += str(self.fftamp14)
        row += self.delim
        row += str(self.fftamp24)
        row += self.delim
        row += str(self.fftamp5)
        row += self.delim
        row += str(self.fftamp15)
        row += self.delim
        row += str(self.fftamp25)
        row += self.delim
        row += str(self.fftamp6)
        row += self.delim
        row += str(self.fftamp16)
        row += self.delim
        row += str(self.fftamp26)
        row += self.delim
        row += str(self.fftamp7)
        row += self.delim
        row += str(self.fftamp17)
        row += self.delim
        row += str(self.fftamp27)
        row += self.delim
        row += str(self.fftamp8)
        row += self.delim
        row += str(self.fftamp18)
        row += self.delim
        row += str(self.fftamp28)
        row += self.delim
        row += str(label)
        row += '\n'
        with open(self.savepath,'a') as f:
            f.write(row)

def main():
    rospy.init_node("mindwave_moter_trainning_record",anonymous=True)
    rospy.loginfo("===Try to stay rest====")
    rospy.loginfo("===Please wait for 30s====")

    
    try:
        rospy.sleep(10.0)
        print('+++ : focus on cneter\n <<<: imagine moving left \n >>>: imagine moving right')
        
        rospy.sleep(10.0)
       
        recored=recorder()

        
    except rospy.ROSInterruptException: pass

    rospy.spin()
    
if __name__ == '__main__':
	main()