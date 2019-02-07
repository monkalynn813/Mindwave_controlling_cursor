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
        self.ax1=self.fig.add_subplot(1,1,1)
        self.fftamp_subscriber=rospy.Subscriber('/mindcontrol/fft',Plotarray,self.fftcallback)
        self.freqamp_subscriber=rospy.Subscriber('/mindcontrol/freq',Plotarray,self.freqcallback)
        self.fftfreq=[]
        self.fftamp=[]
    def fftcallback(self,data):
        self.fftamp=data.data
        
    def freqcallback(self,data):
        self.fftfreq=data.data
    def animate11(self,i):
        self.ax1.clear()
        self.ax1.plot(self.fftfreq,self.fftamp)

def main():
    rospy.init_node("fftploter",anonymous=True)
    
    try:
       
        plot = plotfft()
        ani=animation.FuncAnimation(plot.fig,plot.animate11,interval=100)
        plt.show()
    except rospy.ROSInterruptException: pass

    rospy.spin()
    
if __name__ == '__main__':
	main()