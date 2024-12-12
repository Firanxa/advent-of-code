"""
Advent of Code 2015
Day 15: Science for Hungry People

I tried formulating this as a constrained maximization problem, but solving it 
analytically was too tricky. I solve the maximization by brute force instead: 
Generate all combinations of ingredients whose integer quantities sum to 100, 
compute each cookie score, then take the max.
"""

import re
import numpy as np
from itertools import product
from tqdm import tqdm, trange


# This program won't work on the test file because of the explicit generation 
# of partitions of N = 100 into n = 4 summands.
with open("../_inputs/day15.txt") as f:
    props = f.readlines()

# Parse the ingredient properties.
props = [
    [re.sub(r'[:,]', '', s) for s in prop_list.split()] \
    for prop_list in props]
get_prop_at_index = lambda i: [prop_list[i] for prop_list in props]
str_to_int_list = lambda x: list(map(int, x))

ingredients = get_prop_at_index(0)
capacities = str_to_int_list(get_prop_at_index(2))
durabilities = str_to_int_list(get_prop_at_index(4))
flavors = str_to_int_list(get_prop_at_index(6))
textures = str_to_int_list(get_prop_at_index(8))
calories = str_to_int_list(get_prop_at_index(10))

A = np.array([capacities, durabilities, flavors, textures, calories])

# Generate all partitions of N = 100 as a sum of n = 4 integers.
N = 100
n = 4
partitions = []
# Note that this is actually slower than nested for loops!
# for tup in product(range(1, N), repeat=n):
#     if sum(tup) == N:
#         partitions.append(tup)
for i in trange(1, N):
    for j in range(1, N):
        for k in range(1, N):
            for l in range(1, N):
                if i + j + k + l == N:
                    partitions.append((i, j, k, l))

max_score_without_cals = -np.inf
max_score_with_cals = -np.inf
calorie_requirement = 500
for partition in tqdm(partitions):
    x = np.array(partition)
    
    # PART 1.
    cookie_score = 1
    for a in A[:-1]:
        cookie_score *= max(np.dot(a, x), 0)
    max_score_without_cals = max(cookie_score, max_score_without_cals)
    
    # PART 2.
    if np.dot(A[-1,:], x) == calorie_requirement:
        cookie_score = 1
        for a in A[:-1]:
            cookie_score *= max(np.dot(a, x), 0)
        max_score_with_cals = max(cookie_score, max_score_with_cals)

print(f'PART 1\tBest score without calories: {max_score_without_cals}')
print(f'PART 2\tBest score with {calorie_requirement} calories: {max_score_with_cals}')
