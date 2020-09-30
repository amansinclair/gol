if __name__ == "__main__":
    from gol import run, GOL, PATTERNS
    import numpy as np

    size = 100
    n_patterns = 20
    board = np.zeros((size, size), dtype="int")
    for i in range(n_patterns):
        pattern = np.random.choice(PATTERNS)
        row = np.random.choice(np.arange(size))
        col = np.random.choice(np.arange(size))
        pattern.add_to(board, row, col)
    gol = GOL(board)
    gol.add_random_cells(coverage=0.3)
    run(gol)
