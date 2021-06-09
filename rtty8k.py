import wave
import numpy as np
import array


def read_wave_file(filename, mark_frequency = 914, space_frequency = 1086):
    with wave.open(filename, 'rb') as wave_file:
        sampling_rate = 8000          # Sampling Rate
        window_size = 32           # windows size Integer

        mark_q = array.array('l', [0] * window_size)
        mark_i = array.array('l', [0] * window_size)
        space_q = array.array('l', [0] * window_size)
        space_i = array.array('l', [0] * window_size)
        for j in range(wave_file.getnframes()):
            buf = wave_file.readframes(1)
            array_index = j % window_size
            factor = np.pi * 2.0 * j / sampling_rate
            mark_q[array_index] = int((buf[0]-128) * np.sin(factor * mark_frequency))
            mark_i[array_index] = int((buf[0]-128) * np.cos(factor * mark_frequency))
            space_q[array_index] = int((buf[0]-128) * np.sin(factor * space_frequency))
            space_i[array_index] = int((buf[0]-128) * np.cos(factor * space_frequency))
            mark_value = np.sqrt(sum(mark_q)**2 + sum(mark_i)**2)
            space_value = np.sqrt(sum(space_q)**2 + sum(space_i)**2)
            print(mark_value, space_value, int(mark_value > space_value), sep=",")


if __name__ == '__main__':
    filename = 'rtty3s.wav'  # should be specify the filename.
    read_wave_file(filename)
