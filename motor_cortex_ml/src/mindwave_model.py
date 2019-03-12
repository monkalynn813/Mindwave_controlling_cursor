#!/usr/bin/env python

import rospy
import numpy as np
from std_msgs.msg import Int32
from datastreaming.msg import ChannelData, Plotarray
import csv
import pickle
from std_msgs.msg import String

class classifier():
    def __init__(self):
        self.modelpath = '/home/jingyan/Documents/ME499-WinterProject/mindwave/src/motor_cortex_ml/src/'
        self.model_filename=self.modelpath+'mindwave_model.pkl'
        with open(self.model_filename,'rb') as file:
            self.mindwave_model=pickle.load(file)
        self.mouse_publisher=rospy.Publisher('/mindcontrol/mouse_command',Int32,queue_size=20)
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

        self.inputdata=np.array([[self.fftamp1,self.fftamp11,
                                self.fftamp2,self.fftamp12,
                                self.fftamp3,self.fftamp13,
                                self.fftamp4,self.fftamp14,
                                self.fftamp5,self.fftamp15,
                                self.fftamp6,self.fftamp16,
                                self.fftamp7,self.fftamp17,
                                self.fftamp8,self.fftamp18]])
        # self.inputdata=np.array([[self.fftamp3,self.fftamp4]])
        self.model_command()
    def model_command(self):

        self.command=self.mindwave_model.predict(self.inputdata)[0]
        self.mouse_publisher.publish(self.command)

def main():
    rospy.init_node("mindwave_model")
    
    try:
       
        ml=classifier()

        
    except rospy.ROSInterruptException: pass

    rospy.spin()
    
if __name__ == '__main__':
	main()