"""
Advent of Code 2015
Day 6: Probably a Fire Hazard

NumPy gets this one done quick. I did learn about slice objects, particularly 
with `np.s_`, which are very useful for clean, repeated indexing.
"""

import numpy as np


with open("../_tests/day06.txt") as f:
    instructions = f.read().splitlines()

N = 1000
# PART 1.
light_grid = np.zeros((N, N), dtype='bool')
# PART 2.
brightness_grid = np.zeros((N, N), dtype='int')

for instruction in instructions:
    split_instruction = instruction.split()
    light_change = split_instruction[-4]
    from_coord, to_coord = split_instruction[-3], split_instruction[-1]
    i, j = tuple(map(int, from_coord.split(',')))
    i_next, j_next = tuple(map(int, to_coord.split(',')))

    s = np.s_[i:i_next+1,j:j_next+1] # DRY!
    if light_change == 'on':
        light_grid[s] = True
        brightness_grid[s] = brightness_grid[s] + 1
    elif light_change =='off':
        light_grid[s] = False
        brightness_grid[s] = np.maximum(brightness_grid[s] - 1, 0)
    elif light_change == 'toggle':
        light_grid[s] = ~light_grid[s]
        brightness_grid[s] = brightness_grid[s] + 2

print(f'PART 1\tTotal lights lit: {light_grid.sum()}')
print(f'PART 2\tTotal brightness: {brightness_grid.sum()}')
