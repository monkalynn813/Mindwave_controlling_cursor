#!/usr/bin/env python

from openbci.cyton import OpenBCICyton
import rospy
import numpy as np
from scipy import signal
from scipy.signal import gaussian
from scipy.ndimage import filters

def csd(data,G,H,lam=1e-5,head=1.0):
    #input shape (chan_num * sample)
    ch_num,sample_num=data.shape
    # if G.shape[0]!=G.shape[1] or H.shape[0]!=H.shape[1] or G.shape[0]!=ch_num or H.shape[0]!=ch_num:
    #     ValueError('G,H dimension should be n*n where n is number of channels')
    #     return None
    # else:
    mu=np.mean(data,axis=0) #average among channels 
    Z=(data-np.tile(mu,[ch_num,1]))
    X=np.copy(data)
    G1=np.copy(G)
    head=head*head
    for e in range(G1.shape[0]):
        G1[e,e]=G1[e,e]+lam
    Gi=np.linalg.inv(G1)
    TC=np.zeros(Gi.shape[0])
    for i in range(Gi.shape[0]):
        TC[i]=np.sum(Gi[i])
    sgi=np.sum(TC)
    for p in range(sample_num):
        Cp=np.dot(Gi,Z[:,p])
        c0=np.sum(Cp)/sgi
        C=Cp-(c0*TC.T)
        for e in range(ch_num):
            X[e][p]=np.sum(np.multiply(C,H[e].T))/head
    return X.T


def gaussian_smoothing(data=None, filter_len=None, filter_sigma=None):

    if filter_len is None:
        if len(data) < 20.:
            filter_len = 5
        elif len(data) >= 100.:
            filter_len = 10
        else:
            filter_len = int(len(data) / 10.) + 1
    if filter_sigma is None:
        filter_sigma = filter_len

    gaus = gaussian(filter_len, filter_sigma)
    return filters.convolve1d(data, gaus / gaus.sum(), mode='mirror') 