if __name__ == "__main__":
    from gol import run, GOL
    import numpy as np

    size = 100
    n_fill = int((size ** 2) * 0.8)
    a = np.zeros((size, size))
    idxs = np.random.choice(np.arange(size ** 2), n_fill)
    np.put(a, idxs, 1)
    gol = GOL()
    gol.set_board(a)
    run(gol)
