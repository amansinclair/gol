import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
import matplotlib.pyplot as plt


class GOL:
    def __init__(self, a=None):
        if a:
            self.a = a
        else:
            self.a = self.create_random()

    def scale(self, a, scale=40):
        return a.repeat(scale, axis=0).repeat(scale, axis=1)

    def create_random(self):
        size = 20
        n_fill = int(0.8 * (size ** 2))
        a = np.zeros((size, size), dtype="int")
        idxs = np.random.choice(np.arange(size ** 2), n_fill)
        np.put(a, idxs, 255)
        return a

    def update(self):
        a = self.a.copy()
        for row in range(self.a.shape[0]):
            for col in range(self.a.shape[1]):
                self.a[row, col] = self.update_pixel(a, row, col)
        return self.scale(self.a)

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
    root.after(100, update, root, gol, canvas)


if __name__ == "__main__":
    gol = GOL()
    root = tk.Tk()
    img = ImageTk.PhotoImage(image=Image.fromarray(gol.update()))
    canvas = tk.Canvas(root, width=900, height=900)
    canvas.create_image(50, 50, anchor="nw", image=img)
    canvas.pack()
    update(root, gol, canvas)
    root.mainloop()
