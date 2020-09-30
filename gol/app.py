import time
import tkinter as tk
import numpy as np
from PIL import Image, ImageTk

HEIGHT = 900
WIDTH = 900


class GOL:
    def __init__(self, board=None, size=None, coverage=None):
        if not hasattr(board, "shape"):
            self.board = self.create_random_board(size, coverage)
        else:
            self.board = board
        self.scale = (HEIGHT - 100) // self.board.shape[0]
        self.set_alive_to_white()

    def set_alive_to_white(self):
        self.board[np.where(self.board > 0)] = 255

    def scale_for_screen(self):
        return self.board.repeat(self.scale, axis=0).repeat(self.scale, axis=1)

    def create_random_board(self, size=None, coverage=None):
        size = size if size else 20
        board = np.zeros((size, size), dtype="int")
        coverage = coverage if coverage else 0.5
        self.add_random_cells(coverage, board)
        return board

    def add_random_cells(self, coverage, board=None):
        if not hasattr(board, "shape"):
            board = self.board
        size = board.shape[0]
        coverage = int(coverage * (size ** 2))
        idxs = np.random.choice(np.arange(size ** 2), coverage)
        np.put(board, idxs, 255)

    def update(self):
        board = self.board.copy()
        for row in range(self.board.shape[0]):
            for col in range(self.board.shape[1]):
                self.board[row, col] = self.update_pixel(board, row, col)
        return self.scale_for_screen()

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
    start_array = gol.scale_for_screen()
    img = ImageTk.PhotoImage(image=Image.fromarray(start_array))
    x = (WIDTH - start_array.shape[0]) // 2
    y = (HEIGHT - start_array.shape[1]) // 2
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
    canvas.create_image(x, y, anchor="nw", image=img)
    canvas.pack()
    update(root, gol, canvas)
    root.mainloop()
