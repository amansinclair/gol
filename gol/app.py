import tkinter as tk
from PIL import Image, ImageTk


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(root, width=300, height=300)
        self.canvas.pack(side="top")


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
