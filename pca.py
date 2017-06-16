# pca_base_primary_ambient_decomposition
import wave

from numpy import hamming, zeros, ones, transpose
from scipy.io import wavfile

from sound_util import *

# fs, Input = wavfile.read(file_DIR + 'output.wav')
Input = wave.open(file_DIR + 'output.wav', 'r')
_Input = stereo_to_str(Input)

## window function
N = 4096
win = hamming(N)

sWin = zeros((N, 2))
sWin[:, 0] = win
sWin[:, 1] = win

## parameter
_nFrame = int(Input.getnframes() / N)

xp = zeros((N, 2))
xout_pre = zeros((N, 1))
OutVec = []

_init = 1.e-4
_lambda = 0.8

Lpsd = zeros((N, 1))
Rpsd = zeros((N, 1))
Cpsd = zeros((N, 1))
psd = ones((2, 2, N)) * _init

XL = zeros((N, 2))
XR = zeros((N, 2))

# overlap -add

for i in range(_nFrame):
    # slicing Input as Frame size
    subIn = _Input[i * N: (i + 1) * N, :]
    # fft
    _xp = np.vstack((xp * sWin, subIn * sWin))
    xp = subIn

    XV = np.fft.fft(_xp, N) / len(_xp)

    XL = [XV[1:N, 1], XL[:, 1]]
    XR = [XV[1:N, 2], XR[:, 1]]

    print(len(XV))

    for k in range(N):
        _subIn = [XV[k, 1], XV[k, 2]]
        currP = np.dot(transpose(_subIn), _subIn)
        psd[:, :, k] = psd[:, :, k] * _lambda + (1 - _lambda) * currP
        Cpsd = psd[:, :, k]

Input.close()
