"""
    multimedia project

    editor : ys kim
    cutoff frequency above(or below) threshold
"""

from numpy import *
from scipy import fftpack

from utility.sound_util import *
from utility.plotly_util import showSignalFFT

file_type = '.wav'

input_name = 'saw'
output_name = 'saw_cutoff_frequency'

input_path = file_DIR + input_name + file_type
output_path = file_DIR + output_name + file_type

input = wave.open(input_path, 'r')
nChannels = input.getnchannels()
FrameRate = input.getframerate()
sampWidth = input.getsampwidth()
nFrames = input.getnframes()

if nChannels == 2:
    _Input = stereo2mono(stereo2str(input))
    nChannels = 1
else:
    _Input = wav2str(input)

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

han_stereo = zeros((N, 2))
han_stereo[:, 0] = hanning(N)
han_stereo[:, 1] = hanning(N)

X = np.array([])
Y = np.array([])

_X = np.array([])
_Y = np.array([])


# adjust window function to frequency in each frame
for i in range(_nFrame):

    # check num of channel of sound
    # slice signal as frame size
    if nChannels == 1:
        _subSignal = _Input[i * N: (i + 1) * N]
        _subSignal = _subSignal * hanning(N)
    else:
        break

signal_ = fftpack.rfft(_Input)
cut_freq_signal_ = signal_

threshold = 100000
for i in range(len(cut_freq_signal_)):
    if i < threshold:
        cut_freq_signal_[i] = 0

cut_signal_ = fftpack.irfft(cut_freq_signal_)

cut_freq_signal_ = cut_freq_signal_[range(int(n / 2))]

output = wave.open(output_path, 'w')
output.setparams((nChannels, sampWidth, FrameRate, nFrames, 'NONE', 'not compressed'))

copyWav(output, cut_signal_)

input.close()
output.close()

incVolume(output_name)

# showSignalFFT(cut_signal_, frq, cut_freq_signal_)