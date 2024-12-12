"""
Advent of Code 2015
Day 9: All in a Single Night

I recognized this as a graph problem, which NetworkX made short work of.

At first, I was tripped up by what structure and algorithm to use. My initial
instinct was "minimum spanning tree," but that ignores the problem constraint
that each location must be visited exactly once. The structure I sought is
called a Hamiltonian path (TIL), but NetworkX's implementation works only on
tournament graphs.

Ultimately, I brute forced it by taking advantage of the fact that the graph
representing the route network is actually a complete graph. Each permutation
of the node list is then a Hamiltonian path, so we can iterate over all
permutations, compute the path weights, and take the min and max.
"""

import networkx as nx
from itertools import permutations


with open("../_tests/day09.txt") as f:
    routes = f.read().splitlines()

G = nx.Graph()
for route in routes:
    start, _, end, _, distance = tuple(route.split())
    G.add_edge(start, end, weight=int(distance))

# We can verify that G is complete...
n = G.number_of_nodes()
for _, degree in G.degree:
    assert degree == n - 1

# ... which means every permutation of the nodes is a Hamiltonian path.
total_distances = []
for path in permutations(G.nodes):
    total_distances.append(nx.path_weight(G, path, weight="weight"))

# PART 1.
print(f'PART 1\tShortest total distance: {min(total_distances)}')

# PART 2.
print(f'PART 2\tLongest total distance: {max(total_distances)}')
