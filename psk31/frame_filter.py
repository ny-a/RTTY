
def frame_to_bit_chunks(frame_values, baud_rate=31.25):
    binary_values = frame_to_binary_values(frame_values)
    bit_duration_values = binary_values_to_bit_duration(binary_values)
    bit_values = bit_duration_to_bit_values(bit_duration_values, baud_rate)
    decoded_bit_values = decode_fec(bit_values)
    bit_chunks = bit_values_to_bit_chunks(decoded_bit_values)

    return bit_chunks


def frame_to_binary_values(frame_values):
    for q_value, i_value, time in frame_values:
        yield (int(q_value > 0), int(i_value > 0), time)


def binary_values_to_bit_duration(binary_values):
    previous_q_value = 0
    previous_i_value = 0
    previous_time = 0
    current_q_value = 0
    current_i_value = 0
    current_time = 0
    for q_value, i_value, time in binary_values:
        # use final value after this for loop
        current_q_value = q_value
        current_i_value = i_value
        current_time = time
        if (
            previous_q_value != current_q_value or
            previous_i_value != current_i_value
        ):
            yield (
                previous_q_value,
                previous_i_value,
                current_time - previous_time
            )
            previous_q_value = current_q_value
            previous_i_value = current_i_value
            previous_time = current_time

    yield (current_q_value, current_i_value, current_time - previous_time)


def bit_duration_to_bit_values(bit_duration_values, baud_rate=31.25, minimum_bit_width=0.5):
    duration = 0
    bit_duration = 1 / baud_rate
    minimum_duration = bit_duration * minimum_bit_width
    for q, i, original_duration in bit_duration_values:
        duration += original_duration
        while duration > minimum_duration:
            handle_duration = min(bit_duration, duration)
            width = handle_duration / bit_duration
            yield (q, i, width)
            duration -= handle_duration


GRAY_TABLE = [
    [0, 1],
    [3, 2],
]


def decode_gray_code(q_value, i_value):
    return GRAY_TABLE[q_value][i_value]


def convolutional_encode(old_state, current):
    state = old_state[-4:] + str(current)
    bit1 = int(state[0]) ^ int(state[2]) ^ int(state[3]) ^ int(state[4])
    bit2 = not int(state[0]) ^ int(state[1]) ^ int(state[4])
    return int(bit2) * 2 + int(bit1)


def decode_fec(bit_stream):
    last_input = None
    state = '00000'
    invalid_diffs = []
    for q, i, _ in bit_stream:
        gray_code = decode_gray_code(q, i)
        if last_input is None:
            last_input = gray_code
            yield 0
            continue

        diff = (gray_code - last_input) % 4
        last_input = gray_code
        current_input = None
        if diff == convolutional_encode(state, 0):
            current_input = 0
        elif diff == convolutional_encode(state, 1):
            current_input = 1
        else:
            if len(invalid_diffs) < 5:
                invalid_diffs.append(str(diff))
                continue
            else:
                if all(map(lambda x: x == invalid_diffs[0], invalid_diffs)):
                    current_input = 0
                    state = '00000'
                else:
                    invalid_diffs = []
                    continue

        invalid_diffs = []
        state = state[-4:] + str(current_input)
        yield current_input


def bit_values_to_bit_chunks(bit_values):
    chunk = ''

    for current_value in bit_values:
        if (
            chunk != '' and chunk[-1] == '0' and current_value == 0 or
            chunk == '' and current_value == 0
        ):
            if chunk != '':
                yield chunk.rstrip('0')
                chunk = ''
        else:
            chunk += str(current_value)

    if chunk != '':
        yield chunk.rstrip('0')
