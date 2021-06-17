import sys

from .read_wave_file import read_wave_file 


if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'rtty3s.wav'
    read_wave_file(filename)
