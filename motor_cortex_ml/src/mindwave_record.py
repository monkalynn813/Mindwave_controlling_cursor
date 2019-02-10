#!/usr/bin/env python

import rospy
import numpy as np
from std_msgs.msg import String
from datastreaming.msg import ChannelData, Plotarray
from matplotlib import pyplot as plt
import time
import random


class classifier():
    def __init__(self):

        self.fftamp_subscriber=rospy.Subscriber('/mindcontrol/filtered_data',ChannelData,self.fftcallback)
        self.savepath="/home/jingyan/Documents/ME499-WinterProject/mindwave/src/motor_cortex_ml/data/record.csv"
        self.delim = ','
        self.recordsize=20
        self.detailcounter=0
        self.leftcounter=0
        self.rightcounter=0
        self.centercounter=0
        self.restcounter=0

    def fftcallback(self,data):
        
        self.fftamp1=data.channel1
        self.fftamp2=data.channel2
        self.fftamp3=data.channel3
        self.fftamp4=data.channel4
        self.fftamp5=data.channel5
        self.fftamp6=data.channel6
        self.fftamp7=data.channel7
        self.fftamp8=data.channel8

        if self.detailcounter%150==0 or self.detailcounter==0: #record 150 samples every time call a direction
            self.centercounter=0
            
            if self.leftcounter<self.recordsize and self.rightcounter<self.recordsize:
                call_which=random.randint(0,1) #random pick a direction to imagin 0=left; 1=right
            elif self.leftcounter==self.recordsize and self.rightcounter<self.recordsize: call_which=1
            elif self.leftcounter<self.recordsize and self.rightcounter==self.recordsize: call_which=0
            else: raw_input('Acquisition finished, press ctrl+c to exit')
            
            if call_which==0:
                self.func=self.focusleft
                self.leftcounter+=1
            else: 
                self.func=self.focusright        
                self.rightcounter+=1
        
        if self.restcounter<=150:
            self.rest()
            self.restcounter+=1
            self.detailcounter=1
        elif self.centercounter<=150:
            self.focuscenter()
            self.centercounter+=1
            
            self.detailcounter=1
        else:        
            self.func()
            self.detailcounter=self.detailcounter+1
        
        
    def focuscenter(self):
        rospy.loginfo("focus on center")
        label='0'
        self.writeinfile(label)
    def focusleft(self):
        rospy.loginfo("imagine moving left hand")
        label='-1'
        self.writeinfile(label)
    def focusright(self):
        rospy.loginfo("imagine moving right hand")
        label='1'         
        self.writeinfile(label)
    def rest(self):
        print("take a break")

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
    rospy.init_node("mindwave_classifier",anonymous=True)
    
    try:
       
        ml=classifier()

        
    except rospy.ROSInterruptException: pass

    rospy.spin()
    
if __name__ == '__main__':
	main()