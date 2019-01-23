#!/usr/bin/env python
import os
import rospy
from std_msgs.msg import String
import numpy as np


def main():
    rospy.init_node('motor_imagine',anonymous=True)
    sample_data_sub=rospy.Subsriber('/mindcontrol/channel_data',String,ml_model)
    os.system("xdotool mousemove_relative 10 0")

def ml_model(data):
    pass