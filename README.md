# Mindwave controlling cursor

## Description of the project
The objective	of this project is to control cursor movement on the computer by human intention through brain computer interface (BCI). This will include an electroencephalography (EEG) data collection from EEG monitor. The monitor is expected to track the electrical activity of the brain (mainly focus on motor cortex, the part of brain oversees movement). The project should include signal processing techniques for noise filter and machine learning techniques for multi-class classification. The completed project should allow subjects to think about executing cursor movement and covert signal to real-time command.

## Required liburary
Openbci.cyton
Openbci_python

## ROS package
1. datastreaming
    Read data from EEG monitor and stream data through DSP callback function
2. Machine learning model
    Take sample trainning data from saved csv file and output corresponding command
3. Cursor control 
    Read topic from output of machine learning model and control the cursor movement

## Project Schedule
    <!-- ![Schedule.jpg] -->


## Project block diagram
