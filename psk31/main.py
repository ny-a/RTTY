import sys

from .read_wave_file import read_wave_file


if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'rtty3s.wav'

    with open('{}.csv'.format(filename), 'w') as output:
        for q_value, i_value, time in read_wave_file(filename):
            output.write('{},{},{}\n'.format(int(q_value > 0), int(i_value > 0), time))
