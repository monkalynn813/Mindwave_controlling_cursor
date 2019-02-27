#!/usr/bin/env python

import rospy
import numpy as np
from datastreaming.msg import ChannelData, Plotarray
import time
import random
import sys
import datetime
import os

class recorder():
    def __init__(self):
        savetag='_exp6'
        self.savedir="/home/jingyan/Documents/ME499-WinterProject/mindwave/src/motor_cortex_ml/data/"
        self.savepath=self.savedir+'record'+savetag+'.csv'
        self.delim = ','
        self.recordsize=20
        self.detailsize=250
        self.detailcounter=0
        self.leftcounter=0
        self.rightcounter=0
        self.centercounter=0
        self.restcounter=0

        
        # self.fftamp_subscriber=rospy.Subscriber('/mindcontrol/filtered_data',ChannelData,self.fftcallback)
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

                 
        
        if self.restcounter<self.detailsize:
            if self.leftcounter==self.recordsize and self.rightcounter==self.recordsize:
                raw_input('\n Acquisition finished, press ctrl+c to exit')
            else:
                self.rest()
                self.restcounter+=1
            
        elif self.centercounter<self.detailsize:
            if self.centercounter==0: os.system("xdotool mousemove 960 880")
            self.focuscenter()
            self.centercounter+=1
            self.detailcounter=0

        elif self.detailcounter<self.detailsize:
            if self.detailcounter==0:
                if self.leftcounter<self.recordsize and self.rightcounter<self.recordsize:
                    call_which=random.randint(0,1) #random pick a direction to imagin 0=left; 1=right
                elif self.leftcounter==self.recordsize and self.rightcounter<self.recordsize: call_which=1
                elif self.leftcounter<self.recordsize and self.rightcounter==self.recordsize: call_which=0
                
          
                if call_which==0:
                    self.func=self.focusleft
                    self.leftcounter+=1
                else: 
                    self.func=self.focusright        
                    self.rightcounter+=1  

            if self.detailcounter==self.detailsize-1: 
                self.centercounter=0
                self.restcounter=0   

            self.func()
            self.detailcounter+=1
        
        
    def focuscenter(self):
        sys.stdout.write('\r                                ++++++++++++++                           ')
        sys.stdout.flush()

        label='0'
        self.writeinfile(label)
        
    def focusleft(self):
        sys.stdout.write('\r        <<<<<<<<<<<<<                                                   ')
        sys.stdout.flush()

        label='-1'
        self.writeinfile(label)
        if self.detailcounter==self.detailsize/2 or self.detailcounter==self.detailsize-10: os.system("xdotool mousemove_relative -- -20 0")
    def focusright(self):
        sys.stdout.write('\r                                                            >>>>>>>>>>>')
        sys.stdout.flush()

        label='1'         
        self.writeinfile(label)
        if self.detailcounter==self.detailsize/2 or self.detailcounter==self.detailsize-10: os.system("xdotool mousemove_relative 20 0")
    def rest(self):
        sys.stdout.write('\r                                take a break                           ')
        sys.stdout.flush()

    def writeinfile(self,label):
        row=''
        row += str(self.fftamp1)
        row += self.delim
        row += str(self.fftamp2)
        row += self.delim
        row += str(self.fftamp3)
        row += self.delim
        row += str(self.fftamp4)
        row += self.delim
        row += str(self.fftamp5)
        row += self.delim
        row += str(self.fftamp6)
        row += self.delim
        row += str(self.fftamp7)
        row += self.delim
        row += str(self.fftamp8)
        row += self.delim
        row += str(label)
        row += '\n'
        with open(self.savepath,'a') as f:
            f.write(row)

def main():
    rospy.init_node("mindwave_moter_trainning_record",anonymous=True)
    rospy.loginfo("===Try to stay rest====")
    rospy.loginfo("===Please wait for 30s====")
    rospy.sleep(10.0)
    print('+++ : focus on cneter\n <<<: imagine moving left \n >>>: imagine moving right')
    
    rospy.sleep(20.0)
    
    try:
       
        recored=recorder()

        
    except rospy.ROSInterruptException: pass

    rospy.spin()
    
if __name__ == '__main__':
	main()