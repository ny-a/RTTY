import wave
import math

from .window_sum import WindowSum

def read_wave_file(filename, signed = False, mark_frequency = 914, space_frequency = 1086):
    # 入力ファイルのバイトオーダーを指定する
    # リトルエンディアン: little
    # ビッグエンディアン: big
    byteorder = 'little'

    with wave.open(filename, 'rb') as wave_file:
        # 入力ファイルのサンプリングレートをファイルから取得
        sampling_rate = wave_file.getframerate()
        # 平滑化するウィンドウサイズをサンプリングレートから指定
        window_size = int(sampling_rate / 250)
        # 量子化ビット数をファイルから取得
        bits = (wave_file.getsampwidth() * 8) - 1
        # 符号なしであれば符号付きに変換する
        if signed:
            offset = 0
        else:
            offset = 1 << bits

        # 平滑化をリングバッファを使って高速化する
        # set で与えた今の値を合計に足して、ウィンドウからはみ出た値を引くことで、
        # 毎回全ての合計を出さなくて済むようにしている
        mark_q = WindowSum(window_size)
        mark_i = WindowSum(window_size)
        space_q = WindowSum(window_size)
        space_i = WindowSum(window_size)
        for j in range(wave_file.getnframes()):
            # 符号付き整数値で取得する
            frame_value = int.from_bytes(wave_file.readframes(1), byteorder=byteorder, signed=signed) - offset
            # 経過時刻を計算する
            time = j / sampling_rate
            # 共通の係数を事前に計算する
            factor = math.pi * 2.0 * time
            mark_q.set(int(frame_value * math.sin(factor * mark_frequency)))
            mark_i.set(int(frame_value * math.cos(factor * mark_frequency)))
            space_q.set(int(frame_value * math.sin(factor * space_frequency)))
            space_i.set(int(frame_value * math.cos(factor * space_frequency)))
            # 高速化のために2乗は乗算を使って書く
            mark_value = mark_q.sum * mark_q.sum + mark_i.sum * mark_i.sum
            space_value = space_q.sum * space_q.sum + space_i.sum * space_i.sum
            # mark の強度、space の強度、経過時刻のtupleをyieldする
            yield (mark_value, space_value, time)
