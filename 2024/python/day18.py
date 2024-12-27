"""
Advent of Code 2024
Day 18: RAM Run

Part 1 was straightforward with Dijkstra's algorithm.

I originally solved Part 2 via brute force: Let each byte fall and find the 
(potentially new) Dijkstra path until no path is possible. This runs under 
30 s, which I improved after realizing that the shortest path won't change 
until a byte falls in one of its spaces. Find the first such byte, let all 
bytes through that one fall, and then try to find the Dijkstra path. Repeat 
until no path is possible.
"""

import networkx as nx
import numpy as np


def get_neighbors(x, y, x_max, y_max):
    """Returns a list of points 4-adjacent to the point (x, y)."""
    neighbors = []
    if y < y_max - 1:
        neighbors.append((x, y + 1))
    if x < x_max - 1:
        neighbors.append((x + 1, y))
    if y > 0:
        neighbors.append((x, y - 1))
    if x > 0:
        neighbors.append((x - 1, y))
    
    return neighbors


def find_blocking_byte(path, last_k):
    """Recursively finds the space with the blocking byte."""
    indexes = []
    for space in path:
        try:
            indexes.append(falling_bytes.index(space))
        except ValueError:
            continue
    
    indexes.sort()
    index = indexes[0]
    for k in range(last_k, index + 1):
        space = falling_bytes[k]
        is_corrupted[*space] = True
        if space in G:
            G.remove_node(space)
    
    try:
        path = nx.dijkstra_path(G, start, end)
        last_k = index
        return find_blocking_byte(path, last_k)
    except nx.NetworkXNoPath:
        return falling_bytes[index]


with open("../_tests/day18.txt") as f:
    lines = f.read().splitlines()

falling_bytes = []
for line in lines:
    j, i = tuple(int(x) for x in line.split(','))
    falling_bytes.append((i, j))

# N = 70
N = 6
dims = (N + 1, N + 1)
is_corrupted = np.zeros(dims, dtype='bool')
start = (0, 0)
end = (N, N)

# PART 1.
# k_max = 1024
k_max = 12
for k in range(k_max):
    is_corrupted[*falling_bytes[k]] = True

G = nx.Graph()
for space in np.ndindex(dims):
    if is_corrupted[*space]: continue
    G.add_node(space)
    neighbors = get_neighbors(*space, *dims)
    for neighbor in neighbors:
        if not is_corrupted[*neighbor]:
            G.add_edge(space, neighbor)

path = nx.dijkstra_path(G, start, end)
print(f'PART 1\tLength of shortest path: {len(path) - 1}')

# PART 2.
blocking_byte = find_blocking_byte(path, k_max)
print(f'PART 2\tLocation of blocking byte: {blocking_byte[::-1]}')
