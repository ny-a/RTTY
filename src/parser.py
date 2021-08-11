import sys

from .read_wave_file import read_wave_file
from .frame_filter import frame_to_bit_chunks
from .parse_ita2 import parse_ita2


if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'rtty3s.wav'

    # wav ファイルを読んでフレームごとの信号強度に変換する
    frame_values = read_wave_file(filename, signed=False)
    # フレームごとの信号強度から、5bit のデータビットの chunk に変換する
    bit_chunks = frame_to_bit_chunks(frame_values, baud_rate=45.45, start_bit=0, stop_bit=1)
    # chunk から文字に変換する
    ita2_chars = parse_ita2(bit_chunks)
    for char, _ in ita2_chars:
        # 改行しないで1文字ずつ出力する
        print(char, end='', flush=True)
    print('')
