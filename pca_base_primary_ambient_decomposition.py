from numpy import *
from scipy import fftpack

from utility.sound_util import *
from utility.plotly_util import showSignalFFT

# fs, Input = wavfile.read(file_DIR + 'output.wav')
input = wave.open(file_DIR + 'saw.wav', 'r')
nChannels = input.getnchannels()
FrameRate = input.getframerate()
sampWidth = input.getsampwidth()  # sampling width
nFrames = input.getnframes()
print(nChannels)

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

input.close()

output = wave.open(file_DIR + 'saw_cutoff_frequency.wav', 'w')
output.setparams((nChannels, sampWidth, FrameRate, nFrames, 'NONE', 'not compressed'))

copyWav(output, cut_signal_)

output.close()
