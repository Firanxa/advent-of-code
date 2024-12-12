"""
Advent of Code 2015
Day 1: Not Quite Lisp

A straightforward parsing problem.
"""

with open("../_tests/day01.txt") as f:
    instructions = f.read()

# PART 1.
final_floor = instructions.count('(') - instructions.count(')')
print(f'PART 1\tFinal floor: {final_floor}')

# PART 2.
move = {
    '(': 1,
    ')': -1
}
current_floor = 0
final_step = 0
for i, step in enumerate(instructions):
    current_floor += move[step]
    if current_floor == -1:
        final_step = i + 1
        break
print(f'PART 2\tReached basement at step: {i + 1}')
