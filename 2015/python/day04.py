"""
Advent of Code 2015
Day 4: The Ideal Stocking Stuffer

Straightforward and no surprises.
"""

import hashlib


def solve_day4(K):
    num = 0
    K_zeros = '0' * K
    found = False
    while not found:
        test_input = (key + str(num)).encode('utf-8')
        hashed_input = hashlib.md5(test_input).hexdigest()
        if hashed_input[:K] == K_zeros:
            found = True
        else:
            num += 1

    return num


with open("../_tests/day04.txt") as f:
    key = f.read().strip()

# PART 1.
K = 5
print(f'PART 1\tHash input: {solve_day4(K)}')

# PART 2.
K = 6
print(f'PART 2\tHash input: {solve_day4(K)}')
