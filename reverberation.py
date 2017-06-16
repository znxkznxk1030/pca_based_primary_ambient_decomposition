import wave

from scipy import signal

from sound_util import *

source = wave.open(sound_file, 'r')
nChannels = source.getnchannels()
sampWidth = source.getsampwidth()  # sampling width
FrameRate = source.getframerate()  # sampling rate
nFrames = source.getnframes()

revb = wave.open(file_DIR + 'Reverberation.wav', 'r')

source_str = wav_to_str(source)
revb_str = wav_to_str(revb)

revb_output = signal.lfilter(revb_str, [1.], source_str) / np.max(np.abs(revb_str))

output = wave.open(file_DIR + 'output_revb.wav', 'w')
output.setparams((nChannels, sampWidth, FrameRate, nFrames, 'NONE', 'not compressed'))
copy_wav(output, revb_output)

source.close()
revb.close()
output.close()