#!/usr/bin/env python
import numpy as np
from scipy import signal
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
import matplotlib.pyplot as plt
import csv
import pickle
import datetime

# set path to datasets
datapath = '/home/jingyan/Documents/ME499-WinterProject/mindwave/src/motor_cortex_ml/data/'
csvname =datapath + 'record.csv'
data = np.loadtxt(csvname,delimiter = ',')
savedsp=datapath+'dsp'+str(datetime.datetime.now())+'.csv'
# get input/output pairs
x = data[:,:-1]
y = data[:,-1]
channel_num=8
chunk=4 #matches self.recordsize in mindwave_record.py
fs=250
band=(16,24)

def bandpass(start,stop,data,fs):
    bp_Hz = np.array([start, stop])
    b, a = signal.butter(5, bp_Hz / (fs / 2.0), btype='bandpass')
    return signal.lfilter(b, a, data, axis=0)

def notch(val, data, fs):
    bp_stop_Hz = val + 3.0 * np.array([-1, 1])
    b, a = signal.butter(3, bp_stop_Hz / (fs / 2.0), 'bandstop')
    return signal.lfilter(b, a, data)

def fft(data, fs):
    L = len(data)
    freq = np.linspace(0.0, 1.0 / (2.0 * fs **-1), int(L / 2))
    yi = np.fft.fft(data)#[1:]
    y = yi[range(int(L / 2))]
    # ysample= (2.0*abs(yi/L))[range(int(L/2))]
    return freq, abs(y)
for k in range(channel_num):
    locals()["channel"+str(k+1)]=x[:,k]
#Divide datas to chunks, each chunk coorespond to specific channel with specific y value.
#Total chunk number = channel_num * record_size(chunk) *4
_total_chunk=channel_num*chunk*4
for i in np.unique(y):
    i=int(i)
    locals()['ind_'+str(i+1)]=np.where(y==i)[0] ##left=-1,(ind0) ; right=1,(ind2); focus=0,(ind1);
   
    locals()['ind'+str(i+1)]=[locals()['ind_'+str(int(i+1))][0]]
    for j in range(len(locals()['ind_'+str(i+1)])-1):  
        if (locals()['ind_'+str(i+1)])[j]+1!=(locals()['ind_'+str(i+1)])[j+1]:
            locals()['ind'+str(i+1)].append((locals()['ind_'+str(i+1)])[j])
        if j>1 and (locals()['ind_'+str(i+1)])[j]-1!=(locals()['ind_'+str(i+1)])[j-1]:
            (locals()['ind'+str(i+1)]).append((locals()['ind_'+str(i+1)])[j])
    (locals()['ind'+str(i+1)]).append((locals()['ind_'+str(i+1)])[-1])
    if i!=0 and 2*chunk!=len((locals()['ind'+str(i+1)])):
        print("error: chunk size and interval limit does not match. flag number:",i)
    elif i==0 and 4*chunk!=len((locals()['ind'+str(i+1)])):
        print("error: chunk size and interval limit does not match. flag number: ",i)
    for k in range(channel_num):
        for g in range(int((len((locals()['ind'+str(i+1)])))/2)):
            locals()['channel'+str(k+1)+'_'+str(i+1)+'_chunk'+str(g+1)]=locals()['channel'+str(k+1)][(locals()['ind'+str(i+1)])[2*g]:(locals()['ind'+str(i+1)])[2*g+1]+1]
#DSP for individual chunk
total_chunks=0
row=''
#generate average amplitude of each channel for indivisual label in specific band range
#variable_channel#_label#_chunk#

for i in [-1,0,1]:#np.unique(y):
    i=int(i)
    for k in range(channel_num):
        for g in range(int((len((locals()['ind'+str(i+1)])))/2)):
            data=locals()['channel'+str(k+1)+'_'+str(i+1)+'_chunk'+str(g+1)]
#             locals()['freq'+str(k+1)+'_'+str(i+1)+'_chuank'+str(g+1)],locals()['ffty'+str(k+1)+'_'+str(i+1)+'_chuank'+str(g+1)]=fft(data,fs)
            freq,ffty=fft(data,fs)
            freq_ind=np.where((freq>=band[0])&(freq<=band[1]))[0]
            desired_freq=freq[freq_ind]
            amp_of_desired_freq=ffty[freq_ind]
            average_amp=np.mean(amp_of_desired_freq)
            locals()['average_amp_'+str(k+1)+'_'+str(i+1)+'_'+str(g+1)]=average_amp
            total_chunks+=1
if total_chunks != _total_chunk: print('error: total chunks number does not match with the data acqusition')

for i in [-1,0,1]:#np.unique(y):
    for g in range(int((len((locals()['ind'+str(i+1)])))/2)):
            for k in range(channel_num):
                row+= str(locals()['average_amp_'+str(k+1)+'_'+str(i+1)+'_'+str(g+1)])
                row+=','
            row+=str(i)
            row+='\n'
with open(savedsp,'w') as f:
    f.write(row)
dspdata = np.loadtxt(savedsp,delimiter = ',')
dspx = dspdata[:,:-1]
dspy = dspdata[:,-1]
model=OneVsRestClassifier(SVC(kernel='linear'))
model.fit(dspx,dspy)
score=model.score(dspx,dspy)
print(score)
model_filename='mindwave_model.pkl'
with open(model_filename,'wb') as file:
    pickle.dump(model,file)       