"""
Advent of Code 2024
Day 8: Resonant Collinearity

A surprisingly straightforward grid problem.
"""

import numpy as np
from itertools import combinations


def get_antinodes(antennas, dims, resonant=False):
    """Returns a list of antinode coordinates for the input list of antennas."""
    x_max, y_max = dims
    antinodes = set()
    for (x1, y1), (x2, y2) in combinations(antennas, 2):
        dx, dy = x2 - x1, y2 - y1
        if resonant:
            node1_x, node1_y = x1, y1
            node2_x, node2_y = x2, y2
            while 0 <= node1_x < x_max and 0 <= node1_y < y_max:
                antinodes.add((node1_x, node1_y))
                node1_x, node1_y = node1_x - dx, node1_y - dy
            while 0 <= node2_x < x_max and 0 <= node2_y < y_max:
                antinodes.add((node2_x, node2_y))
                node2_x, node2_y = node2_x + dx, node2_y + dy
        else:
            node1_x, node1_y = x1 - dx, y1 - dy
            node2_x, node2_y = x2 + dx, y2 + dy
            if 0 <= node1_x < x_max and 0 <= node1_y < y_max:
                antinodes.add((node1_x, node1_y))
            if 0 <= node2_x < x_max and 0 <= node2_y < y_max:
                antinodes.add((node2_x, node2_y))

    return list(antinodes)


def place_antinodes(coords, antinode_map):
    for coord in coords:
        antinode_map[coord] = True


with open("../_tests/day08.txt") as f:
    antenna_map = f.read().splitlines()
    antenna_map = np.array([list(line) for line in antenna_map])
    dims = antenna_map.shape

# Hash arrays of the coordinates of antennas according to frequency.
coords_dict = {}
for x, y in np.ndindex(dims):
    if antenna_map[x,y] != '.':
        coords_dict[antenna_map[x,y]] = coords_dict.get(antenna_map[x,y], [])
        coords_dict[antenna_map[x,y]].append((x, y))

antinode_count = 0
antinode_map = np.zeros(dims, dtype='bool')
resonant_antinode_count = 0
resonant_antinode_map = np.zeros(dims, dtype='bool')
for coords_list in coords_dict.values():
    # PART 1.
    antinodes = get_antinodes(coords_list, dims, resonant=False)
    place_antinodes(antinodes, antinode_map)
    # PART 2.
    resonant_antinodes = get_antinodes(coords_list, dims, resonant=True)
    place_antinodes(resonant_antinodes, resonant_antinode_map)

print(f'Number of unique antinodes: {antinode_map.sum()}')
print(f'Number of resonant antinodes: {resonant_antinode_map.sum()}')
