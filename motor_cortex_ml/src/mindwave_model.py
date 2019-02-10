#!/usr/bin/env python

import rospy
import numpy as np
import scipy
from datastreaming.msg import ChannelData, Plotarray
from samplestream import bandpass, notch, fft
import sklearn

class classifier():
    def __init__(self):







def main():
    rospy.init_node("mindwave_model",anonymous=True)
    
    try:
       
        ml=classifier()

        
    except rospy.ROSInterruptException: pass

    rospy.spin()
    
if __name__ == '__main__':
	main()