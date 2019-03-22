# Mindwave controlling cursor

#### _Jingyan Ling_

**-March 2019**

## Description of the project
The objective of this project is to control cursor movement on the computer by human intention through brain computer interface (BCI). This will include an electroencephalography (EEG) data collection from EEG monitor. The monitor is expected to track the electrical activity of the brain (mainly focus on motor cortex, the part of brain oversees movement). The project is mainly focusing on classify left or right movement for now. The completed project should allow subjects to think about executing cursor movement with corresponding hand movement and covert signal to real-time command.

![headset.JPG]()
## Project block diagram
![script_structure.JPG](https://github.com/monkalynn813/Mindwave_controlling_cursor/blob/master/image/script_structure.JPG)

## Hardware

- OpenBCI Ultracortex Mark IV EEG Headset (8 channels)
- OpenBCI Cyton Board (8-channle, 250Hz)
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

## Algorithm and experiment setting
### The electrodes layout 
- based on international 10-20 system. 8 dry electrodes were placed as following:
  - CH1: FC1 (purple)
  - CH2: FC2 (grey)
  - CH3: C3 (Green)
  - CH4: C4 (blue)
  - CH5: Fz (orange)
  - CH6: Cz (yello)
  - CH7: CP1 (red)
  - CH8: CP2 (brown)
![montage.jpg]()

- The electrodes were placed in this way based on the location of motor cortex area of human brain. Channel C3 and C4 are the places where bio potential fire when a person try to move their left or right hand. As known, brain reflex is reversed as actual body, C3 on the left brain is responsible for right hand while C4 and the right for left hand. Other electrodes were placed around C3 and C4 for enhancing signal because of volume conduction and helping with algorithm to get higher SNR. Two ear clips were used to set reference for voltage potential.  

### CSD filter
- CSD filter is a spatial filter used to enhance the weak signal because of volume conduction. It was the first layer of filter once the raw data was streaming from hardware. It was applied at the same rate of data streaming (250Hz). The filter is assigning weight of each channel data based on EEG headset montage. Two matrices with dimension `channel_number x channel_number` were generated and saved as csv files through CSDToolBox in Matlab based on the geometry dimension of human skull. Then such matrices will be used in python implement of CSD filter through `mind_csd.py`.

### Fast Fourier Transform
- FFT is a very common algorithm used in digital signal processing to convert signals in time domain to frequency domain. More information of FFT and DFT could be found [here](https://www.dspguide.com/ch12/2.htm). FFT was implemented through Scipy package in this project. Unlike CSD filter, FFT was applied to streaming data at 50Hz, and with moving window size of 250. In another word, FFT algorithm was applied to each channel's data generated in past one second with moving window having step size of 5. Script `plofft.py` enable a real-time plot of signal in frequency domain for all 8 Channels.

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