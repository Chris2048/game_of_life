#!/usr/bin/env python
"""
Conway's Game of Life, rules:
  1. Any live cell with fewer than two live neighbours dies, as if caused by
     under-population.
  2. Any live cell with two or three live neighbours lives on to the next
     generation.
  3. Any live cell with more than three live neighbours dies, as if by
     overcrowding.
  4. Any dead cell with exactly three live neighbours becomes a live cell,
     as if by reproduction.
  -- http://en.wikipedia.org/wiki/Conway's_Game_of_Life
"""
import collections


class FreqSet(collections.MutableSet):
    """A set impl that can count insert frequencies (removals not incl.).
    """
    def __init__(self):
        self._freq = dict()

    def add(self, item):
        if item not in self._freq:
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
        return item in self._freq

    def freq(self, item):
        return self._freq[item]

    def iter_freq(self):
        return iter(self._freq.items())

    def __repr__(self):
        repr_str = 'FreqSet([' + ', ' \
            .join(i.__repr__() + ';' + str(self.freq(i)) for i in self) + '])'
        return repr_str


class ConwayGameOfLife(object):
    """Class representing Conway's game of life.
    """
    Cell = collections.namedtuple('Cell', "x y")

    @classmethod
    def to_cells(cls, *it):
        """Convert iterable of tuples to set of cells.
        """
        return set(cls.Cell(*i) for i in it)

    def __init__(self):
        # default cell neighbourhood template
        self._cell_nb = self.asciitext_to_template(
            "xxx\nxox\nxxx", include_origin=False)

    @staticmethod
    def asciitext_to_template(asciitext, active_char='x',
                              origin_char='o', include_origin=True):
        """Generate cell-coordinate template from ascii-text.
        """
        # Is there (only one) origin char?
        findex = asciitext.find(origin_char)
        if findex != -1:
            if asciitext[findex+1:].find(origin_char) != -1:
                raise StandardError('Only one origin allowed!')
            lastnl = asciitext[findex::-1].find('\n')
            if lastnl != -1:
                origin_x, origin_y = lastnl - 1, asciitext[:findex].count('\n')
            else:
                # no newline, origin is on first row
                origin_x, origin_y = findex, 0
        else:
            # origin defaults to top-left
            origin_x, origin_y = 0, 0

        cells = []
        lines = asciitext.split('\n')
        for i, line in enumerate(lines):
            for j, line_char in enumerate(line):
                if line_char == active_char or \
                   include_origin and line_char == origin_char:
                    cells.append((j-origin_x, i-origin_y))
        return cells

    def _get_neighbour_cells(self, cell):
        """Return all neighbouring cells of <cell>.
        """
        return set(self.Cell(cell.x + x, cell.y + y) for x, y in self._cell_nb)

    def _get_next_world(self, world):
        """Get next world based on current active cells.
        """
        fworld = FreqSet()
        for cell in world:
            for neighb in self._get_neighbour_cells(cell):
                fworld.add(neighb)
        next_world = set()
        for cell, freq in fworld.iter_freq():
            # 1. Any live cell with fewer than two live neighbours
            #    dies, as if caused by under-population.
            if freq < 2:
                # don't pass cell forward
                pass
            elif freq < 4:
                # 2. Any live cell with two or three live neighbours
                #    lives on to the next generation.
                if cell in world:
                    next_world.add(cell)
                # 4. Any dead cell with exactly three live neighbours
                #    becomes a live cell, as if by reproduction.
                else:
                    if freq == 3:
                        next_world.add(cell)
            # else:
            # 3. Any live cell with more than three live neighbours
            #    dies, as if by overcrowding.
        return next_world

    def conway_gol(self, initial_state):
        """GOL Generator
        """
        active_cells = initial_state
        while True:
            return_count = yield active_cells
            # for testing...
            if return_count is True:
                yield len(active_cells)
            active_cells = self._get_next_world(active_cells)
