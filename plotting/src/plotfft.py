#!/usr/bin/env python

from openbci.cyton import OpenBCICyton
import rospy
import numpy as np
from std_msgs.msg import String
from scipy import signal
from matplotlib import pyplot as plt
from datastreaming.msg import Plotarray
import matplotlib.animation as animation

class plotfft():
    def __init__(self):
        
        self.fig=plt.figure()
        self.ax1=self.fig.add_subplot(111,xlim=(0,60),yscale=("log"))

        self.fftamp_subscriber=rospy.Subscriber('/mindcontrol/fft',Plotarray,self.fftcallback)
        self.freqamp_subscriber=rospy.Subscriber('/mindcontrol/freq',Plotarray,self.freqcallback)
        self.fftfreq=[]
        self.fftamp1=[]
        self.fftamp2=[]
        self.fftamp3=[]
        self.fftamp4=[]
        self.fftamp5=[]
        self.fftamp6=[]
        self.fftamp7=[]
        self.fftamp8=[]
    def fftcallback(self,data):
        self.fftamp1=data.channel1
        self.fftamp2=data.channel2
        self.fftamp3=data.channel3
        self.fftamp4=data.channel4
        self.fftamp5=data.channel5
        self.fftamp6=data.channel6
        self.fftamp7=data.channel7
        self.fftamp8=data.channel8
        
        
    def freqcallback(self,data):
        self.fftfreq=data.channel1
    def animate11(self,i):
        self.ax1.clear()
        self.ax1.plot(self.fftfreq,self.fftamp1,'xkcd:purple')
        self.ax1.plot(self.fftfreq,self.fftamp2,'xkcd:grey')
        self.ax1.plot(self.fftfreq,self.fftamp3,'g-')
        self.ax1.plot(self.fftfreq,self.fftamp4,'xkcd:cyan')
        self.ax1.plot(self.fftfreq,self.fftamp5,'xkcd:orange')
        self.ax1.plot(self.fftfreq,self.fftamp6,'xkcd:yellow')
        self.ax1.plot(self.fftfreq,self.fftamp7,'xkcd:red')
        self.ax1.plot(self.fftfreq,self.fftamp8,'xkcd:brown')
        plt.xlabel('Frequency')
        plt.ylabel('Amplitude')
        plt.xlim(0,60)
        plt.yscale("log")
        plt.grid(True)
        


def main():
    rospy.init_node("fftploter",anonymous=True)
    
    try:
       
        plot = plotfft()

        ani=animation.FuncAnimation(plot.fig,plot.animate11,interval=10)
        plt.show()
    except rospy.ROSInterruptException: pass

    rospy.spin()
    
if __name__ == '__main__':
	main()