import time
import tkinter as tk
import numpy as np
from PIL import Image, ImageTk

HEIGHT = 900
WIDTH = 900


class GOL:
    def __init__(self, board=None, size=None, coverage=None):
        if not hasattr(board, "shape"):
            board = self.create_random_board(size, coverage)
        self.set_board(board)

    def set_board(self, a):
        self.a = a
        self.a[np.where(a > 0)] = 255
        self.scale = (HEIGHT - 100) // self.a.shape[0]

    def scale_array(self, a):
        return a.repeat(self.scale, axis=0).repeat(self.scale, axis=1)

    def create_random_board(self, size=None, coverage=None):
        size = size if size else 20
        coverage = coverage if coverage else int(0.8 * (size ** 2))
        a = np.zeros((size, size), dtype="int")
        idxs = np.random.choice(np.arange(size ** 2), coverage)
        np.put(a, idxs, 255)
        return a

    def update(self):
        a = self.a.copy()
        for row in range(self.a.shape[0]):
            for col in range(self.a.shape[1]):
                self.a[row, col] = self.update_pixel(a, row, col)
        return self.scale_array(self.a)

    def update_pixel(self, a, row, col):
        old_state = a[row, col]
        neighbours = self.get_neighbours(a, row, col)
        n_alive = len(np.where(neighbours > 0)[0])
        if old_state > 0:
            n_alive -= 1
        if old_state > 0 and (n_alive == 2 or n_alive == 3):
            state = 255
        elif old_state == 0 and n_alive == 3:
            state = 255
        else:
            state = 0
        return state

    def get_neighbours(self, a, row, col):
        row_start = max(0, row - 1)
        row_end = min(a.shape[0], row + 2)
        col_start = max(0, col - 1)
        col_end = min(a.shape[1], col + 2)
        return a[row_start:row_end, col_start:col_end]


def update(root, gol, canvas):
    global img
    a = gol.update()
    img = ImageTk.PhotoImage(image=Image.fromarray(a))
    canvas.create_image(50, 50, anchor="nw", image=img)
    root.after(30, update, root, gol, canvas)


def run(gol):
    root = tk.Tk()
    start_array = gol.scale_array(gol.a)
    img = ImageTk.PhotoImage(image=Image.fromarray(start_array))
    x = (WIDTH - start_array.shape[0]) // 2
    y = (HEIGHT - start_array.shape[1]) // 2
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
    canvas.create_image(x, y, anchor="nw", image=img)
    canvas.pack()
    update(root, gol, canvas)
    root.mainloop()
