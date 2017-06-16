import os
import wave

import pygame

from matplotlib import *
from scipy import signal
from numpy import *

from scipy import fftpack

import matplotlib.pyplot as plt
import plotly.plotly as py
import numpy as np
from scipy.signal import fftconvolve

from sound_util import *

ID = 'znxkznxk'
API_KEY = 'sjNJs2P1jDDzlz52fumC'

py.sign_in(ID, API_KEY)

# fs, Input = wavfile.read(file_DIR + 'output.wav')
Input = wave.open(file_DIR + 'saw.wav', 'r')
nChannels = Input.getnchannels()
FrameRate = Input.getframerate()
sampWidth = Input.getsampwidth()  # sampling width
nFrames = Input.getnframes()
print(nChannels)

if nChannels == 2:
    _Input = stereo2mono(stereo_to_str(Input))
    nChannels = 1
else:
    _Input = wav_to_str(Input)

# generate window function

N = 4096
sWin = zeros((N, 2))
sWin[:, 0] = hanning(N)
sWin[:, 1] = hanning(N)

# parameters

_nFrame = int(nFrames / N)
n = int(len(_Input) / nChannels)
k = np.arange(n)
T = n / FrameRate
frq = k / T
frq = frq[range(int(n / 2))]

# print(n)
# for i in range(_nFrame):
#    # slicing Input as Frame size
#    subIn = _Input[i * N: (i + 1) * N, :]
#    _xp = subIn * sWin

han_stereo = zeros((N, 2))
han_stereo[:, 0] = hanning(N)
han_stereo[:, 1] = hanning(N)
# _signal = _Input * han_stereo

X = np.array([])
Y = np.array([])

_X = np.array([])
_Y = np.array([])

for i in range(_nFrame):
    if nChannels == 2:
        _subSignal = _Input[i * N: (i + 1) * N, :]
        _subSignal = _subSignal * han_stereo
    else:
        _subSignal = _Input[i * N: (i + 1) * N]
        _subSignal = _subSignal * hanning(N)

    _subFFT = fftpack.fft(_subSignal)

    Y = np.append(Y, _subFFT)
    X = np.append(X, _subSignal)

    f_signal = fftpack.rfft(_subSignal)
    W = fftpack.fftfreq(_subSignal.size, d=FrameRate)
    cut_f_signal = f_signal

    _threshold = 2

    for k in range(len(f_signal)):
        if W[k] > _threshold:
            cut_f_signal[k] = 0
        else:
            cut_f_signal[k] = f_signal[k]

    _X = np.append(_X, np.fft.irfft(cut_f_signal))
    _Y = np.append(_Y, cut_f_signal)

Y_ = fftpack.fft(X)  # fft computing and normalization

W = fftpack.fftfreq(int(Y_.size / nChannels), d=FrameRate)

print(len(Y_), len(W))

Y_ = Y_[range(int(n / 2))]

signal_ = fftpack.rfft(_Input)
W_ = fftpack.fftfreq(_Input.size, FrameRate)

threshold = 10000

cut_freq_signal_ = signal_

for i in range(len(cut_freq_signal_)):
    if i < threshold:
        cut_freq_signal_[i] = 0


cut_signal_ = fftpack.irfft(cut_freq_signal_)

cut_freq_signal_ = cut_freq_signal_[range(int(n/2))]
_Y = _Y[range(int(n / 2))]


Y = Y[range(int(n / 2))]
# fig, ax = plt.subplots(2, 1)
# ax[0].plot(cut_signal_)
# ax[0].set_xlabel('x')
# ax[0].set_ylabel('y')
#
# ax[1].plot(frq, abs(cut_freq_signal_))
# ax[1].set_xlabel('x')
# ax[1].set_ylabel('y')
#
# plot_url = py.plot_mpl(fig, filename='mpl-basic-fft')

Input.close()

Output = wave.open(file_DIR + 'saw_cutoff_frequency.wav', 'w')
Output.setparams((nChannels, sampWidth, FrameRate, nFrames, 'NONE', 'not compressed'))

copy_wav(Output, cut_signal_)

Output.close()

# pygame.mixer.init()
# pygame.mixer.music.load(noise_file)
# pygame.mixer.music.play()

# while pygame.mixer.music.get_busy():
#    pygame.time.Clock().tick(10)
