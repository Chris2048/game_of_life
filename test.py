#!/usr/bin/env python
"""
Conway's Game of Life, rules:
  1. Any live cell with fewer than two live neighbours dies, as if caused by under-population.
  2. Any live cell with two or three live neighbours lives on to the next generation.
  3. Any live cell with more than three live neighbours dies, as if by overcrowding.
  4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
  -- http://en.wikipedia.org/wiki/Conway's_Game_of_Life
"""
from collections import namedtuple
import collections


Cell = namedtuple('Cell', "x y")

CELL_NEIGHBOURHOOD = (
    (-1,  1), (0,  1), (1,  1),
    (-1,  0),          (1,  0),
    (-1, -1), (0, -1), (1, -1),
)

INITIAL_STATE = set((
    Cell(-1, -1), Cell(0, -1), Cell(1, -1), Cell(-1, 0),
    Cell(0, 0), Cell(1, 0), Cell(-1, 1), Cell(0, 1),
    Cell(1, 1), Cell(2, 1), Cell(0, 2), Cell(1, 2),
    Cell(2, 2), Cell(0, 3), Cell(1, 3), Cell(2, 3),
))


def get_neighbour_cells(cell):
    """Return all neighbouring cells of <cell>.
    """
    return set(Cell(cell.x + x, cell.y + y) for x, y in CELL_NEIGHBOURHOOD)


class FreqSet(collections.MutableSet):
    """A set impl that can count insert frequencies (removals not incl.).
    """
    def __init__(self):
        self._freq = dict()

    def add(self, item):
        if not (item in self._freq):
            self._freq[item] = 1
        else:
            self._freq[item] += 1

    def discard(self, item):
        pass

    def __iter__(self):
        return iter(self._freq)

    def __len__(self):
        return len(self._freq)

    def __contains__(self, item):
        return (item in self._freq)

    def freq(self, item):
        return self._freq[item]

    def iter_freq(self):
        return iter(self._freq.items())

    def __repr__(self):
        repr_str = 'FreqSet(['+', '.join(i.__repr__()+';'+str(self.freq(i)) for i in self)+'])'
        return repr_str


def get_next_world(world):
    """Get next world based on current active cells.
    """
    fworld = FreqSet()
    for c in world:
        for n in get_neighbour_cells(c):
            fworld.add(n)
    next_world = set()
    for c,n in fworld.iter_freq():
        # 1. Any live cell with fewer than two live neighbours
        #    dies, as if caused by under-population.
        if n < 2:
            # don't pass cell forward
            pass
        elif n < 4:
            # 2. Any live cell with two or three live neighbours
            #    lives on to the next generation.
            if c in world:
                next_world.add(c)
            # 4. Any dead cell with exactly three live neighbours
            #    becomes a live cell, as if by reproduction.
            else:
                if n == 3:
                    next_world.add(c)
        # else:
        # 3. Any live cell with more than three live neighbours
        #    dies, as if by overcrowding.
    return next_world

def conway_gol(initial_state=INITIAL_STATE):
    active_cells = initial_state
    while True:
        yield active_cells
        active_cells =  get_next_world(active_cells)

