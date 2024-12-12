"""
Advent of Code 2015
Day 13: Knights of the Dinner Table

Mathematically, the structure of this problem resembles that of Day 9. The 
guests are nodes, and the happiness gains/losses are directed edge weights. 
Since seating the guests in a circle constitutes a Hamiltonian cycle, we can 
iterate over all permutations of the guest list to get a circular seating 
arranagement, compute each one's total happiness, find the maximum possible 
happiness.

Therefore, this solution is O(n!), and I don't think one can do better than 
that.
"""

import numpy as np
from itertools import permutations


def find_total_happiness(M):
    n, _ = M.shape
    total_happiness = -np.inf
    for seating_arrangement in permutations(range(n)):
        happiness = 0
        for k in range(n):
            i = seating_arrangement[k]
            # Mod n ensures a wrap-around to the 0th index in case we are at 
            # k = n - 1.
            j = seating_arrangement[(k + 1) % n]
            happiness += M[i,j] + M[j,i]
        total_happiness = max(happiness, total_happiness)

    return total_happiness


with open("../_tests/day13.txt") as f:
    strings = f.readlines()

# Given n total guests, each guest has (n - 1) potential neighbors, so n can
# be found using the fact that len(strings) = n * (n - 1).
n = int((1 + np.sqrt(1 + 4 * len(strings))) / 2)
M = np.zeros((n, n), dtype='int')
roster = {}

for s in strings:
    s_split = s.split()
    guest_i = s_split[0]
    guest_j = s_split[-1].replace('.', '')

    # Populate and enumerate the guest list.
    i = roster.get(guest_i, len(roster))
    roster[guest_i] = i
    j = roster.get(guest_j, len(roster))
    roster[guest_j] = j

    # M_{ij} is the happiness change for guest i by sitting next to guest j.
    # The boolean check multiplies by +1/-1 for happiness gain/loss.
    happiness_change = int(s_split[3]) * (-1)**(s_split[2] == "lose")
    M[i,j] = happiness_change

# PART 1.
print(f'PART 1\tTotal change in happiness: {find_total_happiness(M)}')

# Part 2.
M_prime = np.zeros((n + 1, n + 1), dtype='int')
M_prime[:n,:n] = M
print(f'PART 2\tNow including you: {find_total_happiness(M_prime)}')
