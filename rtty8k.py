import wave
import numpy as np


filename = 'rtty3s.wav'  # should be specify the filename.
sampling_rate = 8000          # Sampling Rate
mark_frequency = sampling_rate / 914.0     # Mark Frequency 914Hz
space_frequency = sampling_rate / 1086.0    # Space Frequency 1086Hz
window_size = 32           # windows size Integer


with wave.open(filename, 'rb') as wave_file:
    mark_q = []
    mark_i = []
    space_q = []
    space_i = []
    for j in range(wave_file.getnframes()):
        buf = wave_file.readframes(1)
        mark_q.append((buf[0]-128)*np.sin(np.pi*2.0/mark_frequency*j))
        mark_i.append((buf[0]-128)*np.cos(np.pi*2.0/mark_frequency*j))
        space_q.append((buf[0]-128)*np.sin(np.pi*2.0/space_frequency*j))
        space_i.append((buf[0]-128)*np.cos(np.pi*2.0/space_frequency*j))
        mark_value = np.sqrt(sum(mark_q)**2 + sum(mark_i)**2)
        space_value = np.sqrt(sum(space_q)**2 + sum(space_i)**2)
        print(mark_value, space_value, int(mark_value > space_value), sep=",")
        if j > window_size:
            mark_q.pop(0)
            mark_i.pop(0)
            space_q.pop(0)
            space_i.pop(0)
