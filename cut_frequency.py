"""
    multimedia project

    editor : ys kim
    cutoff frequency above(or below) threshold
"""

from numpy import *
from scipy import fftpack

from utility.sound_util import *
from utility.plotly_util import showSignalFFT

input_name = 'saw'
output_name = 'saw_cutoff_frequency'

input_path = file_DIR + input_name + '.wav'
output_path = file_DIR + output_name + '.wav'

input = wave.open(input_path, 'r')
nChannels = input.getnchannels()
FrameRate = input.getframerate()
sampWidth = input.getsampwidth()
nFrames = input.getnframes()

if nChannels == 2:
    source = stereo2mono(stereo2str(input))
    nChannels = 1
else:
    source = wav2str(input)

# generate window function

N = 4096
sWin = zeros((N, 2))
sWin[:, 0] = hanning(N)
sWin[:, 1] = hanning(N)

# parameters

_nFrame = int(nFrames / N)
n = int(len(source) / nChannels)
k = np.arange(n)
T = n / FrameRate
frq = k / T
frq = frq[range(int(n / 2))]

han_stereo = zeros((N, 2))
han_stereo[:, 0] = hanning(N)
han_stereo[:, 1] = hanning(N)

outVec = np.array([])

# adjust window function to frequency in each frame
for i in range(_nFrame):
    if nChannels == 1:
        subSignal = source[i * N: (i + 1) * N]
        subSignal = subSignal * hanning(N)
    else:
        break

    xv = fftpack.rfft(subSignal) * hanning(N)
    xout = fftpack.irfft(xv)
    outVec = np.append(outVec, xout)

signal = fftpack.rfft(source)
cut_freq_signal_ = signal

threshold = 100000
for i in range(len(cut_freq_signal_)):
    if i < threshold:
        cut_freq_signal_[i] = 0

signal_ret = fftpack.irfft(cut_freq_signal_)

cut_freq_signal_ = cut_freq_signal_[range(int(n / 2))]

output = wave.open(output_path, 'w')
output.setparams((nChannels, sampWidth, FrameRate, nFrames, 'NONE', 'not compressed'))

copyWav(output, cut_freq_signal_)

input.close()
output.close()

# edit volume
incVolume(output_name)

showSignalFFT(signal_ret, frq, cut_freq_signal_)
