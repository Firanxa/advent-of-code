"""
Advent of Code 2024
Day 3: Mull It Over

A straightforward regex problem.

Technically, the evaluations for both parts could have been done in the same 
loop. At first, I only extracted `mul(x,y)` since that's all that was needed 
for Part 1. For Part 2, I also found all `do()` and `don't()`s then filtered 
them out so that I could keep the clean map and sum that I originally used for 
Part 1.
"""

import re


# Define a `mul` function so that any extracted string "mul(x,y)" can be 
# evaluated as Python code.
def mul(x, y):
    return x * y


with open("../_tests/day03.txt") as f:
    memory = f.read()

# Find all `mul(x,y)`, `do()` and `don't()` substrings.
instructions = re.findall(r"mul\(\d+,\d+\)|do\(\)|don't\(\)", memory)

# PART 1.
multiplications = [x for x in instructions if x != "do()" and x != "don't()"]
multiplication_sum = sum(map(eval, multiplications))

print(f'PART 1\tSum of multiplications: {multiplication_sum}')

# PART 2.
proceed = True
multiplication_sum = 0
for instruction in instructions:
    if instruction == "do()":
        proceed = True
    elif instruction == "don't()":
        proceed = False
    elif proceed:
        multiplication_sum += eval(instruction)

print(f'PART 2\tSum of multiplications: {multiplication_sum}')
