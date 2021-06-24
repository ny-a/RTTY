import sys

from .read_wave_file import read_wave_file
from .frame_filter import frame_to_bit_chunks


if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'rtty3s.wav'

    with open('{}.csv'.format(filename), 'w') as output:
        frame_values = read_wave_file(filename, signed=False)
        bit_chunks = frame_to_bit_chunks(frame_values, baud_rate=45.45, start_bit=0, stop_bit=1)
        for bit_chunk in bit_chunks:
            print(bit_chunk)
