
def frame_to_bit_chunks(frame_values, baud_rate=45.45, start_bit=0, stop_bit=1):
    binary_values = frame_to_binary_values(frame_values)
    bit_duration_values = binary_values_to_bit_duration(binary_values)
    bit_values = bit_duration_to_bit_values(bit_duration_values, baud_rate)
    bit_chunks = bit_values_to_bit_chunks(bit_values, start_bit, stop_bit)

    return bit_chunks


def frame_to_binary_values(frame_values, threshold=1.0):
    current_binary_value = 0
    for mark_value, space_value, time in frame_values:
        if mark_value * threshold > space_value:
            current_binary_value = 1
        if space_value * threshold > mark_value:
            current_binary_value = 0
        yield (current_binary_value, time)


def binary_values_to_bit_duration(binary_values):
    previous_binary_value = 0
    previous_time = 0
    current_binary_value = 0
    current_time = 0
    for binary_value, time in binary_values:
        # use final value after this for loop
        current_binary_value = binary_value
        current_time = time
        if current_binary_value != previous_binary_value:
            yield (previous_binary_value, current_time - previous_time)
            previous_binary_value = current_binary_value
            previous_time = current_time

    yield (current_binary_value, current_time - previous_time)


def bit_duration_to_bit_values(bit_duration_values, baud_rate=45.45, minimum_bit_width=0.25):
    bit_duration = 1 / baud_rate
    minimum_duration = bit_duration * minimum_bit_width
    duration = 0
    for bit_value, original_duration in bit_duration_values:
        duration += original_duration
        while duration > minimum_duration:
            if duration > bit_duration:
                width = 1
            else:
                width = duration / bit_duration
            yield (bit_value, width)
            duration -= bit_duration


def bit_values_to_bit_chunks(bit_values, start_bit=0, stop_bit=1, lsb_on_left=True):
    previous_bit_value = start_bit
    # uninitialized until first stop_bit -> start_bit occurence
    bit_index = None
    chunk = []

    for current_bit_value, _ in bit_values:
        if bit_index is None:
            if previous_bit_value == stop_bit and current_bit_value == start_bit:
                # find first stop_bit -> start_bit occurence
                bit_index = 0
        else:
            bit_index += 1
            if bit_index <= 5:
                # save data bits
                if lsb_on_left:
                    chunk.append(current_bit_value)
                else:
                    chunk.insert(0, current_bit_value)
            else:
                if bit_index == 6:
                    # data bits ended
                    yield ''.join(str(bit) for bit in chunk)
                    chunk.clear()
                if previous_bit_value == stop_bit and current_bit_value == start_bit:
                    # found next stop_bit -> start_bit
                    bit_index = 0
        previous_bit_value = current_bit_value

