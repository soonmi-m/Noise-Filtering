#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 20:45:44 2020

@author: soonmi
"""


import math as m
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat
music = loadmat('Handel.mat')


t = music['x'][0]
S = music['v'][0] #signal

#plt.plot(time, S, linewidth=0.1)
#plt.xlabel('time')
#plt.ylabel('amplitude')
#plt.title("Handel's Messiah Original")
#plt.show()
#plt.close()

L = t[-1] #length of time
n = 73113 #breaking it up into that many points.

#change to freq domain

K = np.zeros(n, float)
i = 0
while i < n/2+1:
    K[i] = (2.0*m.pi/L)*i
    i = i +1
i = -n/2+1
while i <= -1:
    K[i] = (2.0*m.pi/L)*i
    i = i+1
#print(K) K is the freq

Ks = np.fft.fftshift(K)
St = np.fft.fft(S)

St = np.abs(St)

voc_freq = np.zeros(n, float)
voc_amp = np.zeros(n, float)

i = 0

while abs(K[i]) < 1500:
    voc_freq[i] = K[i]
    voc_amp[i] = St[i]
    i = i +1

stop_freq = i

print(voc_freq, voc_amp)

#plt.plot(voc_freq, voc_amp)
#plt.show()

notes_amp = sorted(voc_amp)[-30:] #the top 30 prominent frequencies in this song
notes_amp = np.array(notes_amp)
print(notes_amp)

i = 0
j = 0
k = 0

notes_freq = np.zeros(30, float)

while j < 30:
    while i < n/2:
        if notes_amp[j] == voc_amp[i]:
            notes_freq[j] = K[i]
#            print("frequency of amp " + str(voc_amp[i]) + " is " + str(notes_freq[j]))
        i = i +1
    j = j+1
    i=0

print(sorted(notes_freq))

##Gabor filter

g = np.zeros(n, float)
w = 2.0 #width -- lower w -> wider window
number_slides = 2 
tslide = np.linspace(0,L,number_slides)
Sgt_notes = np.zeros((number_slides, stop_freq), float)

Sgt_spect = np.zeros((number_slides,n), float)

for slide in range(0,number_slides):

    for i in range(0,n-1):
        x = t[i]
        g[i] = m.exp(-w*(x-tslide[slide])**2)
    
    Sg = g*S #filtered signal
    
    Sgt = np.fft.fft(Sg) 
    Sgt_spect[slide][:] = abs(np.fft.fftshift(Sgt))

    for i in range (0, stop_freq):
        Sgt_notes[slide][i] = Sgt_spect[slide][i]
#
#    plt.plot(K[0:stop_freq],Sgt_notes[slide][:])
#    plt.axis([0,1500,0,7])
#    plt.title('freq gabor vs. amplitude ('+ str(slide+1) + ')')
#    plt.show()

plt.pcolor(tslide, K[0:stop_freq], np.transpose(Sgt_notes))
plt.axis([0,9,400,600])
plt.xlabel('Time')
plt.ylabel('Frequency')
plt.title('Spectrogram with w: ' + str(w) + ' and # slides: ' + str(number_slides))
plt.show()
