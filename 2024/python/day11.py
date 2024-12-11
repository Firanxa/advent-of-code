"""
Advent of Code 2024
Day 11: Plutonian Pebbles

An easy DP problem when memoized. Instead of using any functools helpers, I 
opted to memoize it myself as an exercise.
"""

def blink(stone, n=0, n_max=25, memo={}):
    """
    Returns the total number of stones that a stone at the n-th blink will 
    yield by the (n_max)-th blink. Memoized by stone and blink iteration.
    """
    # Hash results by stone and blink iteration.
    key = (stone, n)
    
    # Base case.
    if n == n_max:
        return 1
    elif key in memo:
        return memo[key]
    
    # Blink rules, in order of priority.
    if stone == 0:
        memo[key] = blink(1, n + 1, n_max, memo)
    elif len(str(stone)) % 2 == 0:
        s = str(stone)
        midpoint = len(s) // 2
        left, right = s[:midpoint], s[midpoint:]
        memo[key] = blink(int(left), n + 1, n_max, memo) + \
            blink(int(right), n + 1, n_max, memo)
    else:
        memo[key] = blink(stone * 2024, n + 1, n_max, memo)

    return memo[key]


with open("../_tests/day11.txt") as f:
    stones = list(map(int, f.read().split()))

# PART 1.
n_blinks = 25
memo = {}
total_stones = sum(blink(stone, 0, n_blinks, memo) for stone in stones)
print(f'PART 1\tAfter {n_blinks} blinks there are: {total_stones} stones')

# PART 2.
n_blinks = 75
memo.clear()
total_stones = sum(blink(stone, 0, n_blinks, memo) for stone in stones)
print(f'PART 2\tAfter {n_blinks} blinks there are: {total_stones} stones')
