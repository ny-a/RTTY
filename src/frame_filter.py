
SPACE = 0
MARK = 1

def frame_to_bit_chunks(frame_values, baud_rate=45.45, start_bit=SPACE, stop_bit=MARK):
    """フレームごとの信号強度からデータビットのまとまりに変換する"""

    binary_values = frame_to_binary_values(frame_values)
    bit_duration_values = binary_values_to_bit_duration(binary_values)
    bit_values = bit_duration_to_bit_values(bit_duration_values, baud_rate)
    bit_chunks = bit_values_to_bit_chunks(bit_values, start_bit, stop_bit)

    return bit_chunks


def frame_to_binary_values(frame_values, threshold=1.0):
    """フレームごとの信号強度から0/1を判定する"""

    # ヒステリシスを持たせるときの前の状態
    current_binary_value = SPACE
    for mark_value, space_value, time in frame_values:
        # mark の強度が space の強度の threshold 倍を越えていれば mark と判断する
        if mark_value > space_value * threshold:
            current_binary_value = MARK
        # space の強度が mark の強度の threshold 倍を越えていれば space と判断する
        if space_value > mark_value * threshold:
            current_binary_value = SPACE
        yield (current_binary_value, time)


def binary_values_to_bit_duration(binary_values):
    """連続する0/1の長さを測る"""

    # 前の値
    previous_binary_value = SPACE
    # 前の値に変化した経過時間
    previous_time = 0
    # 今の値
    current_binary_value = SPACE
    # 今の値に変化した経過時間
    current_time = 0
    for binary_value, time in binary_values:
        # 今の値を代入する
        current_binary_value = binary_value
        current_time = time
        # 前と値が変わっていれば、前の値とその長さを出力する
        if current_binary_value != previous_binary_value:
            yield (previous_binary_value, current_time - previous_time)
            # 今の値を前の値に代入する
            previous_binary_value = current_binary_value
            previous_time = current_time

    # ループ内では最後の値は出力されないので、ここで出力する
    yield (current_binary_value, current_time - previous_time)


def bit_duration_to_bit_values(bit_duration_values, baud_rate=45.45, minimum_bit_width=0.25):
    """短すぎる値を無視したり長い値を1bitごとに分割したりする"""

    # 1bit あたりの時間(秒)
    bit_duration = 1 / baud_rate
    # 基準(minimum_bit_width) bit あたりの時間(秒)
    minimum_duration = bit_duration * minimum_bit_width
    # 最後に出力してからの経過時間
    duration = 0
    for bit_value, original_duration in bit_duration_values:
        # 次の値を読んで、経過時間を足す
        duration += original_duration
        while duration > minimum_duration:
            # 今の値の経過時間が基準を超えている間繰り返す
            if duration > bit_duration:
                # 1bit 分以上続いていたら 1bit 分だけ出力する
                width = 1
            else:
                # 1bit より少なければ、全部出力する
                width = duration / bit_duration
            yield (bit_value, width)
            # 出力した分だけ経過時間を減らす
            duration -= bit_duration


def bit_values_to_bit_chunks(bit_values, start_bit=SPACE, stop_bit=MARK, lsb_on_left=True):
    """1bit ごとの値からデータビットを抽出する

    bit_index|ビットの役割
    ---------|----------
    0        |スタートビット
    1        |データビット
    2        |データビット
    3        |データビット
    4        |データビット
    5        |データビット
    6        |ストップビット

    bit_index が 1-5の範囲のみを出力する
    """
    # 前のデータ とりあえずスタートビットとしておく
    previous_bit_value = start_bit
    # データビットの何番目を処理しているかを数えておく
    # はじめはどのタイミングか分からないので None にしておく
    bit_index = None
    # データビットを貯める
    chunk = []

    for current_bit_value, _ in bit_values:
        if bit_index is None:
            # 初期状態、まだデータのタイミングが分かっていない
            if previous_bit_value == stop_bit and current_bit_value == start_bit:
                # 1つ目のストップビット→スタートビットの遷移を検出
                # タイミングが決まる
                bit_index = 0
        else:
            # データのタイミングが分かっている
            # 次のビットを読む
            bit_index += 1
            if bit_index <= 5:
                # 5個目まではデータビットなので読む
                # この if はデータビットの順番が 12345 か 54321 のどちらにも対応するためのもの
                if lsb_on_left:
                    # list への append は最後に追加する
                    chunk.append(current_bit_value)
                else:
                    # list への insert(0) は最初に追加する
                    chunk.insert(0, current_bit_value)
            else:
                # データビットが終わった
                if bit_index == 6:
                    # ストップビットが来るはず あんまり気にしないで貯めたデータを出力する
                    yield ''.join(str(bit) for bit in chunk)
                    # データを空にしておく
                    chunk.clear()
                if previous_bit_value == stop_bit and current_bit_value == start_bit:
                    # スタートビットが来たので状態をリセットする
                    bit_index = 0
        previous_bit_value = current_bit_value

