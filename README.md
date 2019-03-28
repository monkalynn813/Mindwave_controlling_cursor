# Mindwave controlling cursor

#### _Jingyan Ling_

**-March 2019**

## Description of the project
The objective of this project is to control cursor movement on the computer by human intention through brain computer interface (BCI). This will include an electroencephalography (EEG) data collection from EEG monitor. The monitor is expected to track the electrical activity of the brain (mainly focus on motor cortex, the part of brain oversees movement). The project is mainly focusing on classify left or right movement for now. The completed project should allow subjects to think about executing cursor movement with corresponding hand movement and covert signal to real-time command.


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
![montage.jpg](https://github.com/monkalynn813/Mindwave_controlling_cursor/blob/master/image/montage.jpg)

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
![training_procedure](https://github.com/monkalynn813/Mindwave_controlling_cursor/blob/master/image/training_procedure.png)
- Since an `1x 24` matrix is sent at 50Hz to recording node, each run will contains 30 tasks, which contains 7.5s x 50= 375 samples. First 10 tasks in each run will be fixed cross on screen only for baseline purpose. Not all data in each run will be recorded in csv file, however, the samples with corresponding label (left=1, right=2, baseline=0) will be written in csv file after 0.5s of cue on screen, and will stop such writing before break. This process is providing feasibility of well-performed feature extraction.
### Baselines Standardize
- Instead of common standardizing technique. A baseline data was computed from training data to extract feature better from class 'left' and 'right'. The baseline contains the normalized information of subject opening eyes without thinking any hands' movement in each experiment. The mean of large amount of samples within baseline label was computed to set as reference for left and right signal comparison. In order to standardize data, difference between samples and baseline information will be divided by baseline value as well. In another word, the data was represented as percentage drop or rise according to subject's electroencephalography baseline data.  
### Post Filter
- A debouncing-like filter was the last layer of filter before actual mouse command. The filter stores last two command sent from classification model node and generate new command if needed based on history of mouse command. This filter provides a smoother performance of mouse movement even with some misclassification command sent from previous node.

## High-level description and included packages/ files
### Required Package List
- [rqt_image_view](http://wiki.ros.org/rqt_image_view)
- [plotjuggler](http://wiki.ros.org/plotjuggler)

### High level description 
The project can be functional mainly rely on three individual packages. A brief explanation of each package function is as following:
- `datastreaming` : Streams raw data from EEG monitor (Ultracortex Mark IV headset and USB Dongle), applies CSD filter and compute FFT matrix, publishes filtered data at rostopic `'/mindcontrol/average_amp'`
- `motor_cortex_ml`: Subscribes data from `datastream`, executes training experiment, and generates fitted model for classifications. This package also contains function of classify real-time data to mouse command published at rostopic `'/mindcontrol/mouse_command'`.
- `cursor_control`: Subscribes mouse command from `mindwave_model.py` and applies debouncing filter before executing actual mouse movement.
- `plotting` : This is a side package use for observe EEG data in frequency domain when argument `plot` in roslaunch file is set to be True.
### Customized ROS message
- ChannelData.msg
- Plotarray.msg
  
### Package Breakdown
#### ***`datastreaming`***
#### Nodes
- `samplestream.py`: This node streams raw EEG data based on OpenBCI cyton python library. It takes two arguments in roslaunch file, argument `mode` is used for different filters applied as callback function of raw data streaming, while argument `plot` is a bool value indicating whether user need a real-time FFT plot. Callback filter function `filter_fft` is mainly used in development of this package, it generates average amplitude of signal in certain bandwidth ranges. Other two callback filter functions `filter_bp` and `no_filter` is also available in node, `filter_bp` generates bandpass filtered data at the same rate as streaming raw data (250Hz) and publishes data through rostopic `'/mindcontrol/filtered_data'`, while `no_filter` is publishing data to rostopic without any DSP. The node also loads two matrices generated from CSDToolBox in Matlab to apply CSD filter to every incomig set of raw data. 
- `playback.py`: This node is used to simulate real-time data streaming from recorded EEG raw data. It acts the same way as `samplestream.py` but easier for debugging and demo purpose.
- `mind_csd.py`: This is a python script for implementation of CSD filter. It takes raw data and two matrices for spatial filter computation.
#### Message 
- `ChannelData.msg` message was generated for channel data communication among ROS packages in this project. This message has 24 attributes, those indicate for signal amplitude for 8 channels in 3 different bandwidth ranges.

- `Plotarray.msg` message takes float number in array for real-time FFT data plotting purpose.
#### Other Files
- `G_mon1.csv & H_mon1.csv`: Two matrices generated by Matlab through CSDToolBox based on information of individual's EEG montage.
#### ***`motor_cortex_ml`***
#### Data directory
- Directory for recorded training data. (set as .gitignore). Contact me if you want to have access of data set.
#### Nodes
- `mindwave_record.py`: This node runs when argument of `mode` in roslaunch file is set to be `record`. It subscribes rostopic `'/mindcontrol/average_amp'` and generates a GUI along with the training procedure mentioned in Algorithm session. Meaningful data after 0.5s of cue will be written in csv file and store in `data` directory with corresponding labels. (each sample has size of `1 x 25`). The GUI showed below is generated by publishing picture message to `rqt_image_view`.
![gui_preview](https://github.com/monkalynn813/Mindwave_controlling_cursor/blob/master/image/gui_preview.gif)
- `mindwave_model.py`: This node runs when argument of `mode` in roslaunch file is set to be `fft`. It also subscribes the rostopic `'/mindcontrol/average_amp'` and loads the model and baseline information generated by `mindwave_model_csd_fft.ipynb`. The node applies baseline standardizing followed by setting input data into classification model. Also it publishes real-time mouse command at 50Hz at `'/mindcontrol/mouse_command'`.
- `mindwave_traning.py`: This node runs data pre-processing techniques if raw/filtered data was stored for deep-learning or post DSP purpose.
#### Other Files
- `mindwave_model_csd_fft.ipynb`: This is jupyter notebook used to generate classification model. `load_data` function loads csv files created by `mindwave_record.py`. `base_line_fft` computes baseline information and applies baseline standardizing on training data. This notebook provides several classifiers from Scikit-learn with tuned arguments, user can choose whichever classifier generate best fit performance depend on individual's training data. The script also create a `basedline_ref.csv` file in src/ directory for real-time model usage.
- `mindwave_model.pkl`: The classification model generated by `mindwave_model_csd_fft.ipynb` and loaded by `mindwave_model.py` through Pickle for real-time classification
- `baseline_ref.csv`: The baseline standardizing information for real-time data pre-processing usage. 
#### ***`cursor_control`***
#### Node
- `cursorcontrol.py`: This node subscribes `'/mindcontrol/mouse_command'` and applies post debouncing filter before sending actual command for mouse movement.
  
#### Launch file
- `mind_control_cursor.launch`: This is the launch file for entire project. It takes two arguments `mode` and `plot`. Nodes `samplestream.py`, `mindwave_model.py`, and `cursorcontrol.py` will be executed if `mode` is set to be `fft`. Nodes `samplestream.py`, `modewave_record.py`, and `rqt_image_view` will be executed if `mode` is set to be `recored`. If argument `plot` is set to be True, node `plotfft` will be executed as well. 
## Demo Video and package run instruction 
### Demo video
One can find demo video [here](https://youtu.be/WFwUBeXI7JE)
### Project run instruction

 * > roslaunch cursor_control mind_control_cursor.launch mode:=fft
 * > mode:=record  #to record training data
 * > mode:=fft   #to run control mode after classifier trained
 * > plot:=True  #to show real-time FFT diagram 

## Issue and Improvement
- The project will be improved later to adapt more directional movement classification
- More subject will be included in training procedure for robustness 
- A better and faster react of command will lead to a much clearer demo video
- Such movement control command will be executed on Rethink Baxter Robot later.