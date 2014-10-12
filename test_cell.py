import unittest
from test import Cell, get_neighbour_cells, get_alive_neighbours, get_potential_states
from test import update, should_living_live, should_dead_live


class TestCell(unittest.TestCase):
    def test(self):
        expected = (
            Cell(-1, 1),
            Cell(0, 1),
            Cell(1, 1),
            Cell(1, 0),
            Cell(1, -1),
            Cell(0, -1),
            Cell(-1, -1),
            Cell(-1, -0)
        )
        got = get_neighbour_cells(Cell(0, 0))
        self.assertEqual(
            got,
            set(expected)
        )

    def test_get_alive_neighbours(self):
        cell = Cell(0, 0)
        world = (
            Cell(-1, 1),
            Cell(1, -1),
            Cell(0, 2),
            Cell(0, 0)
        )
        expected = set((Cell(-1, 1), Cell(1, -1)))
        self.assertEqual(
            get_alive_neighbours(Cell(0, 0), set(world)),
            expected
        )

    def test_get_potential_states(self):
        world = set((Cell(0, 0), Cell(1, 2)))
        expected = set((
            Cell(-1, -1),
            Cell(0, -1),
            Cell(1, -1),
            Cell(-1, 0),
            Cell(0, 0),
            Cell(1, 0),
            Cell(-1, 1),
            Cell(0, 1),
            Cell(1, 1),
            Cell(2, 1),
            Cell(0, 2),
            Cell(1, 2),
            Cell(2, 2),
            Cell(0, 3),
            Cell(1, 3),
            Cell(2, 3),
        ))
        self.assertEqual(get_potential_states(world), expected)

    def test_should_living_live(self):
        self.assertEqual(should_living_live(1), False)
        self.assertEqual(should_living_live(2), True)
        self.assertEqual(should_living_live(3), True)
        self.assertEqual(should_living_live(4), False)

    def test_should_dead_live(self):
        self.assertEqual(should_dead_live(3), True)

    def test_update(self):
        return
        world = set()
        self.assertEqual(update(world), [])
