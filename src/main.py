import sys

from .read_wave_file import read_wave_file 


if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'rtty3s.wav'

    with open('{}.csv'.format(filename), 'w') as output:
        for mark_value, space_value, j in read_wave_file(filename):
            output.write('{},{},{}\n'.format(mark_value, space_value, int(mark_value > space_value)))
