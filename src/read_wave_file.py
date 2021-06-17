import wave
import numpy as np

from .window_sum import WindowSum 

def read_wave_file(filename, signed = False, mark_frequency = 914, space_frequency = 1086):
    byteorder = 'little'

    with wave.open(filename, 'rb') as wave_file:
        sampling_rate = wave_file.getframerate()
        window_size = int(sampling_rate / 250)
        bits = (wave_file.getsampwidth() * 8) - 1
        if signed:
            offset = 0
        else:
            offset = 1 << bits

        mark_q = WindowSum(window_size)
        mark_i = WindowSum(window_size)
        space_q = WindowSum(window_size)
        space_i = WindowSum(window_size)
        for j in range(wave_file.getnframes()):
            frame_value = int.from_bytes(wave_file.readframes(1), byteorder=byteorder, signed=signed) - offset
            factor = np.pi * 2.0 * j / sampling_rate
            mark_q.set(int(frame_value * np.sin(factor * mark_frequency)))
            mark_i.set(int(frame_value * np.cos(factor * mark_frequency)))
            space_q.set(int(frame_value * np.sin(factor * space_frequency)))
            space_i.set(int(frame_value * np.cos(factor * space_frequency)))
            mark_value = np.sqrt((mark_q.sum)**2 + (mark_i.sum)**2)
            space_value = np.sqrt((space_q.sum)**2 + (space_i.sum)**2)
            print(mark_value, space_value, int(mark_value > space_value), sep=",")
