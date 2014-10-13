#!/usr/bin/env python
from collections import namedtuple
Cell = namedtuple('Cell', "x y")


def get_neighbour_cells(cell):
    ret = []
    for x in range(-1, 2):
        for y in range(-1, 2):
            ret.append(Cell(cell.x + x, cell.y + y))
    ret.remove(cell)
    return set(ret)


def get_alive_neighbours(cell, world):
    return get_neighbour_cells(cell) & world


def get_potential_states(world):
    ret = set()
    for cell in world:
        ret.add(cell)
        for neighbour in get_neighbour_cells(cell):
            ret.add(neighbour)
    return ret


def should_living_live(alive_count):
    if alive_count < 2:
        return False
    elif alive_count == 2:
        return True
    elif alive_count == 3:
        return True
    elif alive_count > 3:
        return False


def should_dead_live(alive_count):
    if alive_count == 3:
        return True


def update(world):
    new_world = set()

    alive_cells = world
    dead_cells = get_potential_states(world) - world

    for cell in alive_cells:
        alive_count = get_alive_neighbours(cell, world)
        if should_living_live(alive_count):
            new_world.add(cell)

    for cell in dead_cells:
        alive_count = get_alive_neighbours(cell, world)
        if should_dead_live(alive_count):
            new_world.add(cell)
    return new_world
