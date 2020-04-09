if __name__ == "__main__":
    from gol import run, GOL, Blinker, Toad, Beacon, Ant, LWSS, Pulsar
    import numpy as np

    size = 100
    a = np.zeros((size, size), dtype="int")
    items = [Blinker(), Toad(), Beacon(), Ant(), LWSS(), Pulsar()]
    locs = [(20, 90), (30, 30), (70, 70), (10, 10), (20, 20), (70, 20)]
    for loc, item in zip(locs, items):
        item.add_to(a, *loc)
    gol = GOL()
    gol.set_board(a)
    run(gol)
