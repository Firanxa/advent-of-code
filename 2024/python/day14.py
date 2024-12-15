"""
Advent of Code 2024
Day 14: Restroom Redoubt

Part 1 was straightforward, but I lost a lot of time from not realizing I was 
forgetting to parse the minus sign for negative numbers! The logic here can 
also be applied in Part 2. Given an initial position p and velocity v, the 
robot will be at position p + vt after t seconds. To keep the indexes in 
bounds, take each coordinate modulo its axis's dimension.

I needed a hint for Part 2. One Reddit solution calculated safety factors up 
to some time T and noted a significant dip in safety factor at the time that 
turned out to be the answer. I tried this, but it slowed down too much, and I
gave up.

Another solution observed that the Christmas tree pattern is unique in that 
every robot occupies its own tile. This is what I tried and got the answer 
with, but it's unclear if this is provably correct or just a coincidence. The 
dimensions (103, 101) must matter, since this method definitely doesn't work
on the test input.
"""

import numpy as np


with open("../_tests/day14.txt") as f:
    lines = f.read().splitlines()

parse = lambda s: int(''.join([x for x in s if x.isdigit() or x == '-']))

ps = []
vs = []
for line in lines:
    split_line = line.split()
    p_line, v_line = split_line[0], split_line[1]
    # Must reverse the split to get (y, x) ordering, since NumPy is row major.
    p_line_split = p_line.split(',')[::-1]
    v_line_split = v_line.split(',')[::-1]
    p = np.array([parse(s) for s in p_line_split])
    v = np.array([parse(s) for s in v_line_split])
    ps.append(p)
    vs.append(v)
ps = np.array(ps)
vs = np.array(vs)

# Input dimensions are (103, 101), test dimensions are (7, 11).
# m, n = (103, 101)
m, n = (7, 11)
space = np.zeros((m, n), dtype='int')
T = 100
new_ps = ps + vs * T
for p in new_ps:
    p[0] %= m
    p[1] %= n
    space[*p] += 1

half_m = m // 2
half_n = n // 2
safety_factor = space[:half_m,:half_n].sum() * \
    space[:half_m,half_n+1:].sum() * \
    space[half_m+1:,:half_n].sum() * \
    space[half_m+1:,half_n+1:].sum()

print(f'PART 1\tSafety factor: {safety_factor}')

# PART 2.
t = 0
unique_p_count = 0
while unique_p_count != len(ps):
    space = np.zeros_like(space, dtype='bool')
    t += 1
    new_ps = ps + vs * t
    for p in new_ps:
        p[0] %= m
        p[1] %= n
        space[*p] = True
    unique_p_count = space.sum()

print(f'PART 2\tChristmas tree occurs at: t = {t}')
