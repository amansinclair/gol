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

    def set_board(self, board):
        self.board = board
        self.board[np.where(board > 0)] = 255
        self.scale = (HEIGHT - 100) // self.board.shape[0]

    def scale_array(self, board):
        return board.repeat(self.scale, axis=0).repeat(self.scale, axis=1)

    def create_random_board(self, size=None, coverage=None):
        size = size if size else 20
        board = np.zeros((size, size), dtype="int")
        coverage = coverage if coverage else int(0.8 * (size ** 2))
        return add_random_cells(board, coverage)

    def add_random_cells(self, board, coverage):
        size = board.shape[0]
        idxs = np.random.choice(np.arange(size ** 2), coverage)
        np.put(board, idxs, 255)
        return board

    def update(self):
        board = self.board.copy()
        for row in range(self.board.shape[0]):
            for col in range(self.board.shape[1]):
                self.board[row, col] = self.update_pixel(board, row, col)
        return self.scale_array(self.board)

    def update_pixel(self, board, row, col):
        old_state = board[row, col]
        neighbours = self.get_neighbours(board, row, col)
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

    def get_neighbours(self, board, row, col):
        row_start = max(0, row - 1)
        row_end = min(board.shape[0], row + 2)
        col_start = max(0, col - 1)
        col_end = min(board.shape[1], col + 2)
        return board[row_start:row_end, col_start:col_end]


def update(root, gol, canvas):
    global img
    a = gol.update()
    img = ImageTk.PhotoImage(image=Image.fromarray(a))
    canvas.create_image(50, 50, anchor="nw", image=img)
    root.after(30, update, root, gol, canvas)


def run(gol):
    root = tk.Tk()
    start_array = gol.scale_array(gol.board)
    img = ImageTk.PhotoImage(image=Image.fromarray(start_array))
    x = (WIDTH - start_array.shape[0]) // 2
    y = (HEIGHT - start_array.shape[1]) // 2
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
    canvas.create_image(x, y, anchor="nw", image=img)
    canvas.pack()
    update(root, gol, canvas)
    root.mainloop()
