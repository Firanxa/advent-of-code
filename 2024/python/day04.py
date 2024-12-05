"""
Advent of Code 2024
Day 4: Ceres Search

I can't think of a faster (or at least, more straightforward) solution than 
to find all the X's and A's and then branch outward. It looks messy, but 
logically it was easy to implement, and it gets the answers fast. My only 
head-banging moment was to get the diagonals right in Part 2.

NumPy wasn't really necessary, but it makes indexing easier for me to write 
and follow.
"""

import numpy as np


def get_words(x, y, x_max, y_max, d=4):
    words = []
    # Top right.
    if (y - d + 1 >= 0) and (x + d - 1 < x_max):
        words.append([grid[x+k,y-k] for k in range(d)])
    # Bottom right.
    if (y + d - 1 < y_max) and (x + d - 1 < x_max):
        words.append([grid[x+k,y+k] for k in range(d)])
    # Bottom left.
    if (y + d - 1 < y_max) and (x - d + 1 >= 0):
        words.append([grid[x-k,y+k] for k in range(d)])
    # Top left.
    if (y - d + 1 >= 0) and (x - d + 1 >= 0):
        words.append([grid[x-k,y-k] for k in range(d)])
    # Up.
    if y - d + 1 >= 0:
        words.append([grid[x,y-k] for k in range(d)])
    # Right.
    if x + d - 1 < x_max:
        words.append([grid[x+k,y] for k in range(d)])
    # Down.
    if y + d - 1 < y_max:
        words.append([grid[x,y+k] for k in range(d)])
    # Left.
    if x - d + 1 >= 0:
        words.append([grid[x-k,y] for k in range(d)])
    
    # Return the words in each of the eight directions as a list of strings.
    for i, word in enumerate(words):
        words[i] = ''.join(word)
    
    return words


def is_xmas(word):
    return word == "XMAS" or word == "SAMX"


def is_cross_mas(x, y, x_max, y_max):
    # Only interior points can be the center of a cross.
    if (0 < x < x_max - 1) and (0 < y < y_max - 1):
        diag_1 = ''.join([grid[x+k,y+k] for k in [-1, 0, 1]])
        diag_2 = ''.join([grid[x+k,y-k] for k in [1, 0, -1]])
        return (diag_1 == "MAS" or diag_1 == "SAM") and \
            (diag_2 == "MAS" or diag_2 == "SAM")
    return False


with open("../_tests/day04.txt") as f:
    lines = f.read().splitlines()

grid = np.array([list(line) for line in lines])
dims = grid.shape

# PART 1.
X_indexes = zip(*np.where(grid == 'X'))
xmas_count = 0
for i, j in X_indexes:
    words = get_words(i, j, *dims)
    xmas_count += sum([is_xmas(word) for word in words])

print(f'PART 1\tXMAS appears: {xmas_count} times')

# PART 2.
A_indexes = zip(*np.where(grid == 'A'))
cross_count = 0
for i, j in A_indexes:
    cross_count += is_cross_mas(i, j, *dims)

print(f'PART 2\tNumber of X-MAS crosses: {cross_count}')
