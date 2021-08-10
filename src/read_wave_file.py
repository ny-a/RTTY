import wave
import math

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
            time = j / sampling_rate
            factor = math.pi * 2.0 * time
            mark_q.set(int(frame_value * math.sin(factor * mark_frequency)))
            mark_i.set(int(frame_value * math.cos(factor * mark_frequency)))
            space_q.set(int(frame_value * math.sin(factor * space_frequency)))
            space_i.set(int(frame_value * math.cos(factor * space_frequency)))
            mark_value = mark_q.sum * mark_q.sum + mark_i.sum * mark_i.sum
            space_value = space_q.sum * space_q.sum + space_i.sum * space_i.sum
            yield (mark_value, space_value, time)
