import wave
import math

from .window_sum import WindowSum

def read_wave_file(filename, signed = False, frequency = 1000):
    byteorder = 'little'

    with wave.open(filename, 'rb') as wave_file:
        sampling_rate = wave_file.getframerate()
        window_size = int(sampling_rate / 200)
        bits = (wave_file.getsampwidth() * 8) - 1
        if signed:
            offset = 0
        else:
            offset = 1 << bits

        q_window = WindowSum(window_size)
        i_window = WindowSum(window_size)
        for j in range(wave_file.getnframes()):
            frame_value = int.from_bytes(wave_file.readframes(1), byteorder=byteorder, signed=signed) - offset
            time = j / sampling_rate
            factor = math.pi * 2.0 * time * frequency
            q_window.set(frame_value * math.sin(factor))
            i_window.set(frame_value * math.cos(factor))
            yield (q_window.sum, i_window.sum, time)
