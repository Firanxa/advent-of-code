"""
Advent of Code 2024
Day 7: Bridge Repair

Advent of Brute Force continues...

If there are N nums per target, then there are N - 1 operations in the 
equation. I cycle through all permutations of the operations (so O(2^(N - 1)) 
for Part 1, O(3^(N - 1)) for Part 2) and evaluate left to right. Given this 
input size, this program runs in ~12 s. (Slower than I believe is possible for 
this problem, but also faster than yesterday's).

A smarter way to do this might've been to work backwards. Since all targets 
and nums are integers, we can immediately eliminate a permutation if the last 
num doesn't evenly divide the target. Then proceed right to left, trying to 
reduce the target to the first num and breaking once there's an uneven 
division.
"""

from itertools import product


def calibrate(target, nums):
    """
    Determines whether the target can be expressed by left-to-right addition, 
    multiplication, and concatenation of nums. First evalutes if possible with 
    addition and multiplication (Part 1), then if possible with concatenation 
    as well (Part 2).
    
    Returns a tuple (bool, bool).
    """
    # Base case is that only one number is entered with the target.
    N = len(nums)
    if N == 1:
        is_valid = target == nums[0]
        return is_valid, is_valid

    # Part 1: Calibrate using only + and *.
    is_valid = False
    op_permutations = product([0, 1], repeat=N-1)
    for op_permutation in op_permutations:
        test_value = nums[0]
        for i, op in zip(range(1, N), op_permutation):
            if op == 0:
                test_value += nums[i]
            elif op == 1:
                test_value *= nums[i]
            # The test value is nondecreasing going from left to right.
            if test_value > target:
                break
        if test_value == target:
            is_valid = True
            break

    # If a calibration succeeds in Part 1, it'll also succeed in Part 2.
    if is_valid:
        return is_valid, is_valid

    # Part 2: Calibrate using +, *, and ||.
    is_valid_with_concat = False
    op_permutations = product([0, 1, 2], repeat=N-1)
    for op_permutation in op_permutations:
        test_value = nums[0]
        for i, op in zip(range(1, N), op_permutation):
            if op == 0:
                test_value += nums[i]
            elif op == 1:
                test_value *= nums[i]
            elif op == 2:
                test_value = int(str(test_value) + str(nums[i]))
            if test_value > target:
                break
        if test_value == target:
            is_valid_with_concat = True
            break
    
    # Note that getting to this point means this can only return (False, False) 
    # or (False, True).
    return is_valid, is_valid_with_concat


with open("../_inputs/day07.txt") as f:
    lines = f.readlines()

total_calibration_result = 0
total_calibration_result_with_concats = 0
for line in lines:
    split_line = line.split(":")
    target = int(split_line[0])
    nums = list(map(int, split_line[1].split()))
    
    is_valid, is_valid_with_concat = calibrate(target, nums)
    # PART 1.
    if is_valid:
        total_calibration_result += target
    # PART 2.
    if is_valid_with_concat:
        total_calibration_result_with_concats += target

print(f'PART 1\tTotal_calibration_result: {total_calibration_result}')
print(f'PART 2\tWith concatenations: {total_calibration_result_with_concats}')
