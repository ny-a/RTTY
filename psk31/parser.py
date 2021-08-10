import sys

from .read_wave_file import read_wave_file
from .frame_filter import frame_to_bit_chunks
from .parse_varicode import parse_varicode


if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'psk31.wav'

    frame_values = read_wave_file(filename, signed=False)
    bit_chunks = frame_to_bit_chunks(frame_values)
    chars = parse_varicode(bit_chunks)
    for char, _ in chars:
        print(char, end='', flush=True)
    print('')
