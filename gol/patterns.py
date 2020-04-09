import numpy as np


class Pattern:
    rows = [0]
    cols = [0]

    def __init__(self):
        n_rows = np.max(self.rows) + 1
        n_cols = np.max(self.cols) + 1
        self.mask = np.zeros((n_rows, n_cols))
        self.mask[(self.rows, self.cols)] = 1

    def add_to(self, a, row, col):
        a[row : row + self.mask.shape[0], col : col + self.mask.shape[1]] = self.mask


class Blinker(Pattern):
    rows = [0, 0, 0]
    cols = [0, 1, 2]


class Toad(Pattern):
    rows = [0, 0, 0, 1, 1, 1]
    cols = [1, 2, 3, 0, 1, 2]


class Beacon(Pattern):
    rows = [0, 0, 1, 1, 2, 2, 3, 3]
    cols = [0, 1, 0, 1, 2, 3, 2, 3]


class Pulsar(Pattern):
    rows = [0, 0, 0, 2, 2, 3, 3, 4, 4, 5, 5, 5]
    cols = [2, 3, 4, 0, 5, 0, 5, 0, 5, 2, 3, 4]

    def __init__(self):
        super().__init__()
        oh, ow = self.mask.shape
        h = (oh * 2) + 1
        w = (ow * 2) + 1
        self.half_mask = np.zeros((oh, w))
        self.half_mask[:oh, :ow] = self.mask
        self.half_mask[:oh, ow + 1 :] = np.flip(self.mask, axis=1)
        self.mask = np.zeros((h, w))
        self.mask[0:oh, :] = self.half_mask
        self.mask[oh + 1 :, :] = np.flip(self.half_mask, axis=0)


class Ant(Pattern):
    rows = [0, 1, 2, 2, 2]
    cols = [1, 2, 0, 1, 2]


class LWSS(Pattern):
    rows = [0, 0, 0, 0, 1, 1, 2, 3, 3]
    cols = [1, 2, 3, 4, 0, 4, 4, 0, 3]
