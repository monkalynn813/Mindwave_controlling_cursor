# Mindwave controlling cursor

#### _Jingyan Ling_

**-March 2019**

## Description of the project
The objective of this project is to control cursor movement on the computer by human intention through brain computer interface (BCI). This will include an electroencephalography (EEG) data collection from EEG monitor. The monitor is expected to track the electrical activity of the brain (mainly focus on motor cortex, the part of brain oversees movement). The project is mainly focusing on classify left or right movement for now. The completed project should allow subjects to think about executing cursor movement with corresponding hand movement and covert signal to real-time command.

## Project block diagram
![script_structure.JPG](https://github.com/monkalynn813/Mindwave_controlling_cursor/blob/master/image/script_structure.JPG)

## Hardware

- OpenBCI Ultracortex Mark IV EEG Headset (8 channels)
- OpenBCI Cyton Board
- OpenBCI USB Dongle
- Rubber ball (2 ea.)
  
## Software Requirement

- Linux 18.04
- ROS Melodic
- RFduino Bluetooth modules 
- Python
- Scipy
- OpenCV2
- Scikit-learn
- xdotool
- Pickle
- CSDToolBox (Matlab)
- Openbci_python library

## Algorithm 


## High-level description and included packages/ files
### ROS package
1. datastreaming
    Read data from EEG monitor and stream data through DSP callback function
2. Machine learning model
    Take sample trainning data from saved csv file and output corresponding command
3. Cursor control 
    Read topic from output of machine learning model and control the cursor movement




## Run program by using roslaunch file

 * > roslaunch cursor_control mind_control_cursor.launch mode:=fft
 * > mode:=record  #to record trainning data
 * > mode:=fft   #to run control mode after classifier trained
 * > plot:=True  #to show real-time FFT diagram 

https://youtu.be/PIS7Em5LzI4
<iframe width="560" height="315" src="https://www.youtube.com/embed/PIS7Em5LzI4" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>