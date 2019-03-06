#!/usr/bin/env python
import numpy as np
from scipy import signal
from sklearn.preprocessing import LabelBinarizer
import csv


    # set path to datasets
datapath = '/home/jingyan/Documents/ME499-WinterProject/mindwave/src/motor_cortex_ml/data/'
for run in range(1,7): #6runs for each session
    savetag='_exp10_sec1_run'+str(run)
    csvname =datapath + 'record'+savetag+'.csv'
    data = np.loadtxt(csvname,delimiter = ',')
    if run==1:
        x = data[:,:-1]
        y = data[:,-1]
    else:
        x=np.append(x,data[:,:-1],axis=0)
        y=np.append(y,data[:,-1],axis=0)
channel_num=8
chunk=60
fs=250
band=(0.5,100)
notchval=60
samplesize=7.5*250

train_data,train_labels=data_preposcessing(x,y,chunk,fs,band,notchval,samplesize)

def bandpass(start,stop,data,fs):
    bp_Hz = np.array([start, stop])
    b, a = signal.butter(5, bp_Hz / (fs / 2.0), btype='bandpass')
    return signal.lfilter(b, a, data, axis=0)

def notch(val, data, fs):
    bp_stop_Hz = val + 3.0 * np.array([-1, 1])
    b, a = signal.butter(3, bp_stop_Hz / (fs / 2.0), 'bandstop')
    return signal.lfilter(b, a, data)

def data_preposcessing(x,y,chunk,fs,band,nothval,samplesize,channel_num=8):
    #Divide datas to chunks, each chunk coorespond to specific channel with specific label.
    #Total chunk number = channel_num * record_size(chunk) *3
    _total_chunk=channel_num*chunk*3

    for k in range(channel_num):
        locals()["channel"+str(k+1)]=x[:,k]

    eventsplit=[]
    for u in range(int(chunk*3)):
        event_locator=u*samplesize
        eventsplit.append(int(event_locator))

    for i in np.unique(y):
        i=int(i)
        locals()['ind'+str(i+1)]=[]
    for split in eventsplit:
        label_finder=int(y[split])
        locals()['ind'+str(label_finder+1)].append([split,int(split+samplesize-1)])
    for i in np.unique(y):
        i=int(i)
    #     locals()['ind_'+str(i+1)]=np.where(y==i)[0] ##left=-1,(ind0) ; right=1,(ind2); focus=0,(ind1);

    #     locals()['ind'+str(i+1)]=[locals()['ind_'+str(int(i+1))][0]]  
    #     for j in range(len(locals()['ind_'+str(i+1)])-1):  
    #         if (locals()['ind_'+str(i+1)])[j]+1!=(locals()['ind_'+str(i+1)])[j+1]:
    #             locals()['ind'+str(i+1)].append((locals()['ind_'+str(i+1)])[j])
    #         if j>1 and (locals()['ind_'+str(i+1)])[j]-1!=(locals()['ind_'+str(i+1)])[j-1]:
    #             (locals()['ind'+str(i+1)]).append((locals()['ind_'+str(i+1)])[j])
    #     (locals()['ind'+str(i+1)]).append((locals()['ind_'+str(i+1)])[-1])   #find boundry of events

        if chunk!=len((locals()['ind'+str(i+1)])):
            print("error: chunk size and interval limit does not match. flag number:",i)
        for k in range(channel_num):
            for g in range(int(len((locals()['ind'+str(i+1)])))):
                locals()['channel'+str(k+1)+'_'+str(i+1)+'_chunk'+str(g+1)]=locals()['channel'+str(k+1)][(locals()['ind'+str(i+1)])[g][0]:(locals()['ind'+str(i+1)])[g][1]+1]

    total_chunks=0
    #apply bp and notch filter
    #variable_channel#_label#_chunk#

    for i in np.unique(y):
        i=int(i)
        for k in range(channel_num):
            for g in range(int(len((locals()['ind'+str(i+1)])))):
                data=locals()['channel'+str(k+1)+'_'+str(i+1)+'_chunk'+str(g+1)]
                bp_filtered=bandpass(band[0],band[1],data,fs) #apply band pass filter
                channel_filtered=notch(notchval,bp_filtered,fs)
                locals()['bp_filtered'+str(k+1)+'_'+str(i+1)+'_'+str(g+1)]=channel_filtered
                total_chunks+=1
    if total_chunks != _total_chunk: print('error: total chunks number does not match with the data acqusition')
    ##################CNN input matrix generation#################################
    labels=[]
    for i in np.unique(y): 
        i=int(i)
        for g in range(int(len((locals()['ind'+str(i+1)])))):
            for k in range(channel_num):
                data=locals()['channel'+str(k+1)+'_'+str(i+1)+'_chunk'+str(g+1)]
                if k==0:
                    CNNmatrices_mergechn=[data]
                else:
                    CNNmatrices_mergechn=np.append(CNNmatrices_mergechn,[data],axis=0)
            if g==0 and i==-1: CNNmatrices=CNNmatrices_mergechn.reshape(1,CNNmatrices_mergechn.shape[0],CNNmatrices_mergechn.shape[1])
            else: CNNmatrices=np.append(CNNmatrices,CNNmatrices_mergechn.reshape(1,CNNmatrices_mergechn.shape[0],CNNmatrices_mergechn.shape[1]),axis=0)
            labels=np.append(labels,[i])
    #     _shape=CNNmatrices.shape
    #     CNN_input=CNNmatrices.reshape(_shape[0],1,_shape[1],_shape[2])
    lb = LabelBinarizer()
    label_enc=lb.fit_transform(labels)
    return CNNmatrices,labels