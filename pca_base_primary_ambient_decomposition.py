from numpy import *
from scipy import fftpack, signal

from utility.sound_util import *
from utility.plotly_util import showSignalFFT

file_type = '.wav'

# path of files (.wav)

input_name = 'Fe_sp_1'
output_name = 'primary_output'
hl_name = 'L0e' + '00' + '0a'
hr_name = 'R0e' + '00' + '0a'
noi_name = 'W2'

input_path = file_DIR + input_name + '.wav'
output_path = file_DIR + output_name + '.wav'
hl_path = file_DIR + hl_name + '.wav'
hr_path = file_DIR + hr_name + '.wav'
noi_path = file_DIR + noi_name + '.wav'

# open source file and get params

input = wave.open(input_path)
nChannels = input.getnchannels()
FrameRate = input.getframerate()
sampWidth = input.getsampwidth()  # sampling width
nFrames = input.getnframes()

# open impulse file and change str

hl = wav2str(wave.open(hl_path, 'r'))
hr = wav2str(wave.open(hr_path, 'r'))
noise = wav2str(wave.open(noi_path, 'r'))

# check sound channel

if nChannels == 2:
    source = wav2str(input)
    source = stereo2mono(source)
else:
    source = wav2str(input)
    lenSource = len(source)
    source2 = np.transpose(np.vstack((signal.lfilter(hl, [1.], source) / np.max(np.abs(hl)),
                                      signal.lfilter(hr, [1.], source) / np.max(np.abs(hr))
                                      )))

# generate noise

# noi = np.random.uniform(low=1, high=2, size=(len_source, 2))

# synthesize noise

noise = noise[:lenSource, :]
source2 = synthesize(source2, noise)

# create stereo window function
# - hanning function (nfft : 4096, N : 2048)

nfft = 516
N = int(nfft / 2)

hanning2 = zeros((N, 2))
hanning2[:, 0] = hanning(N)
hanning2[:, 1] = hanning(N)

hanning1 = hanning2

hanning2 = np.vstack((hanning2, hanning2))

# define frequency parameters

n = int(len(source) / nChannels)
k = np.arange(n)
T = n / FrameRate
frq = k / T
frq = frq[range(int(n / 2))]

# define parameters

frame = int(lenSource / N)

init = 1.e-4
lamb = 0.8

xp = zeros((N, 2))

xout_pre = zeros(N)
XL = zeros((N, 1))
XR = zeros((N, 1))

psd = ones((2, 2, N)) * init

Sest = zeros(N)
Nlest = zeros((N, 1))
Nrest = zeros((N, 1))

OutVec = empty(0)

for i in range(frame):
    subSignal = source2[i * N: (i + 1) * N, :]
    print(i)
    XVL = fftpack.rfft(subSignal[:, 0])
    XVR = fftpack.rfft(subSignal[:, 1])
    # TV = fftpack.rfft(subSignal)
    # print(shape(np.vstack((xp, subSignal))))
    xp = subSignal

    # XL = np.transpose(np.vstack((XV[:N, 0], XL[:, 0])))
    # XR = np.transpose(np.vstack((XV[:N, 1], XR[:, 0])))

    # XL = np.transpose(XV[:N, 0])
    # XR = np.transpose(XV[:N, 1])

    for k in range(N):
        subIn = vstack((XVL[k], XVR[k]))
        currP = dot(subIn.transpose(), subIn)
        # print(currP)

        psd[:, :, k] = psd[:, :, k] * lamb + (1 + lamb) * currP
        Cpsd = psd[:, :, k]

        # compute eigenvalue & eigenvector

        eigVal, eigVec = np.linalg.eig(Cpsd)
        # print(eigVal, eigVec)
        pan = eigVec[:, 1]

        # get min,max eigenvalue

        inside_root = sqrt(pow(abs(Cpsd[0, 0] - Cpsd[1, 1]), 2)
                           + pow(abs(Cpsd[0, 1]), 2) * 4)
        min_eig = (Cpsd[0, 0] + Cpsd[1, 1] - inside_root) / 2
        max_eig = (Cpsd[0, 0] + Cpsd[1, 1] + inside_root) / 2

        # print(Cpsd[0, 1], Cpsd[0, 0] + Cpsd[1, 1], inside_root)

        # estimate primary source
        # Sest[k] = (XVL[k] + XVR[k]) / 2
        Sest[k] = pan[0] * XVL[k] + pan[1] * XVR[k]
        scaling = sqrt((max_eig - min_eig) / (min_eig + init))
        Sest[k] = Sest[k] * scaling

        # estimate ambient source

        Nlest[k] = XVL[k] - (1 - sqrt(min_eig / (max_eig + init))
                             * Sest[k] * pan[0])
        Nrest[k] = XVR[k] - (1 - sqrt(min_eig / (max_eig + init))
                             * Sest[k] * pan[1])

    # ifft
    # print(shape(XV[:N, 0]))
    ConjVec = np.append(XVL[:N], XVL[N - 1::-1])
    # ConjVec = np.append(Sest, Sest[::-1])

    # print(shape(ConjVec))

    xout = fftpack.irfft(Sest)
    # print(shape(xout), shape(xout_pre))
    # print(shape(Sest[::-1]))

    # xout = fftpack.irfft(TV)
    # print(shape(xout))
    # xout = xout.transpose()

    # out = xout_pre + xout[:N]
    # xout_pre = xout[N:]

    OutVec = append(OutVec, xout)
    # print(OutVec)

print('process end : copy start')
ext_primary = OutVec[N + 1:]
print(ext_primary)
output = wave.open(output_path, 'w')
output.setparams((2, sampWidth, FrameRate, nFrames, 'NONE', 'not compressed'))

copyWav2(output, source2)

input.close()
output.close()
