#!/usr/bin/env python
"""Tests for Game of Life.
"""
import unittest
# TODO put methods etc. in object, and just import that. Also rename 'test.py'
from test import *


class TestCell(unittest.TestCase):

    def test_get_neighbour_cells(self):
        """Test get_neighbour_cells.
        """
        expected = set((
            Cell(-1, 1), Cell(0, 1), Cell(1, 1), Cell(1, 0),
            Cell(1, -1), Cell(0, -1), Cell(-1, -1), Cell(-1, -0)
        ))
        self.assertEqual(get_neighbour_cells(Cell(0, 0)), expected)

    def test_get_next_world(self):
        """Test get_next_world.
        """
        world = set((Cell(0, 0), Cell(1, 1), Cell(0, 1)))
        # TODO check manually...
        expected = set([Cell(0, 1), Cell(1, 0), Cell(0, 0), Cell(1, 1)])
        self.assertEqual(get_next_world(world), expected)

    def test_generator(self):
        """Test conway generator.
        """
        world = set((Cell(0, 0), Cell(1, 1), Cell(0, 1), Cell(1, 2), Cell(1, 0)))
        x = conway_gol(initial_state=world)
        # Run for 3 generations
        for i in xrange(3):
            print x.next()
        # TODO check manually...
        # check 4th generation
        expected = set([Cell(1, 1), Cell(2, 1)])
        self.assertEqual(x.next(), expected)


if __name__ == '__main__':
    unittest.main()


