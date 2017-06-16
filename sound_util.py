import numpy as np
import wave
import os

import struct

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_DIR = "sound/"

aiz = "00"
hl_file = file_DIR + "L0e0" + aiz + "a.wav"
hr_file = file_DIR + "R0e0" + aiz + "a.wav"
sound_file = "sound/Fe_sp_1.wav"
noise_file = "sound/W2.wav"


def stereo2mono(src: np.array):
    ret = np.array([])
    d = (src[:, 0] + src[:, 1]) / 2

    return d


def mono_to_stereo(dest: wave.Wave_write, src_l: str, src_r: str):
    duration = min(len(src_l), len(src_r))
    for i in range(duration):
        l = src_l[i]
        r = src_r[i]
        packed_value = struct.pack('<hh', np.int16(l), np.int16(r))
        dest.writeframes(packed_value)


def copy_wav(dest: wave.Wave_write, src):
    for i in src:
        packed_value = struct.pack('<h', np.int16(i))
        dest.writeframes(packed_value)


def read_wav_as_str(file_dir, mode):
    try:
        source = wave.open(file_dir, mode)
        source_raw = source.readframes(-1)
        source_raw = np.fromstring(source_raw, 'Int16')

        print(file_dir, source.getnchannels())

        return source_raw
    except FileExistsError as e:
        print(e)
    except FileNotFoundError as e:
        print(e)


def wav_to_str(input_sound: wave.Wave_read):
    try:
        source_signal = input_sound.readframes(-1)
        source_signal = np.fromstring(source_signal, 'Int16')
        return source_signal
    except ConnectionError as e:
        print(e)
    except FileExistsError as e:
        print(e)
    except FileNotFoundError as e:
        print(e)


def stereo_to_str(input: wave.Wave_read):
    source_signal = input.readframes(-1)
    source_signal = np.fromstring(source_signal, 'Int16')

    source_signal = np.array(np.reshape(source_signal, (input.getnframes(), 2)))

    return source_signal
