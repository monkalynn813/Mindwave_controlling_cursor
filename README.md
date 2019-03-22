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

## Algorithm & Research Setting
### Montage 
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
- FFT is a very common algorithm used in digital signal processing to convert signals in time domain to frequency domain. More information of FFT and DFT could be found [here](https://www.dspguide.com/ch12/2.htm). FFT was implemented through Scipy package in this project. Unlike CSD filter, it was applied to streaming data at 50Hz, and with moving window size of 250. In another word, FFT algorithm was applied to each channel's data generated in past one second with moving window having step size of 5. Script `plofft.py` enable a real-time plot of signal in frequency domain for all 8 Channels. A matrix of size `sample_size (250) x channel_number (8)` will be generated afterwards, three bandwidth range then will be filtered out based on following information of human Electroencephalography data.
  - Alpha Wave (8 ~ 13 Hz): Active when relaxed/reflecting. Also associated with inhibition control
  - Beta Wave (16 ~ 30 Hz): Active when thinking, focus, high alert, and anxious
  - Theta Wave (4 ~ 8 Hz): Active when trying to repress a response or action
- The average of signal amplitude within such three frequency ranges will be computed and sent to classification node. A matrix of size `1x 24` will be generated at rate of 50Hz.
  
### Training Data 
- Script `mindwave_record.py` was created to help with recording training data for machine learning classification. One experiment contains two sessions and each sessions contains 6 runs. The procedure of each run is described as following figure.
- ![training_procedure]()
- Since an `1x 24` matrix is sent at 50Hz to recording node, each run will contains 7.5s x 50= 375 samples. Not all data in each run will be recorded in csv file, however, the samples with corresponding label (left=1, right=2, baseline=0) will be written in csv file after 0.5s of cue on screen, and will stop such writing before break. This process is providing feasibility of well-performed feature extraction.
### Baselines
- Instead of common standardizing technique. A baseline data was computed from training data to extract feature better from class 'left' and 'right'. The baseline contains the normalized information of subject opening eyes without thinking any hands' movement in each experiment. The mean of large amount of samples within baseline label was computed to set as reference for left and right signal comparison. In order to standardize data, difference between samples and baseline information will be divided by baseline value as well. In another word, the data was represented as percentage drop or rise according to subject's electroencephalography baseline data.  
### Post Filter
- A denouncing-like filter was the last layer of filter before actual mouse command. The filter stores last two command sent from classification model node and generate new command if needed based on history of mouse command. This filter provides a smoother performance of mouse movement even with some misclassification command sent from previous node.

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