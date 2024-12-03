"""
Advent of Code 2024
Day 1: Historian Hysteria

This didn't require NumPy, but it made the list slicing and operations so much
easier.
"""

import numpy as np


with open("../_tests/day01.txt") as f:
    text = f.readlines()

for i, line in enumerate(text):
    text[i] = line.split()
nums = np.array(text, dtype='int')

# PART 1.
left_list = np.sort(nums[:,0])
right_list = np.sort(nums[:,1])
total_distance = np.abs(left_list - right_list).sum()

print(f'PART 1\tTotal distance is: {total_distance}')

# PART 2.
right_counts = {}
for num in right_list:
    right_counts[num] = right_counts.get(num, 0) + 1

similarity_score = 0
for num in left_list:
    similarity_score += num * right_counts.get(num, 0)

print(f'PART 2\tSimilarity score is: {similarity_score}')
