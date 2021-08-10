import array

class WindowSum:
    INITIAL_VALUE = 0

    def __init__(self, window_size: int):
        self.max_index = window_size - 1
        self.buf = array.array('l', [self.INITIAL_VALUE] * window_size)
        self.current_index = self.INITIAL_VALUE
        self.sum = self.INITIAL_VALUE
    
    def set(self, value: int):
        self.sum += value - self.buf[self.current_index]
        self.buf[self.current_index] = value

        if self.current_index == self.max_index:
            self.current_index = self.INITIAL_VALUE
        else:
            self.current_index += 1
