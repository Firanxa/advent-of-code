"""
Advent of Code 2024
Day 15: Warehouse Woes

The logic for Part 1 was clear but tedious to implement. I was tripped up by 
the edge case of pushing a series of boxes into a wall.

Part 2 to come... I didn't get to finish either part on time because I was 
sick this day :/
"""

import numpy as np


def is_box(x, y):
    return warehouse[x,y] == 'O'


def is_empty(x, y):
    return warehouse[x,y] == '.'


with open("../_tests/day15.txt") as f:
    lines = f.read().splitlines()

warehouse = []
instructions = []
reading_instructions = False
for line in lines:
    if not line:
        reading_instructions = True
    elif not reading_instructions:
        warehouse.append(list(line))
    else:
        instructions.append(line)

warehouse = np.array(warehouse)
dims = warehouse.shape
instructions = ''.join(instructions)

# Use (y, x) ordering for NumPy arrays.
directions = {
    '<': np.array([0, -1]),
    '^': np.array([-1, 0]),
    '>': np.array([0, 1]),
    'v': np.array([1, 0])
}

current_position = np.argmax(warehouse == '@')
current_position = np.unravel_index(current_position, dims)

for instruction in instructions:
    move = directions[instruction]
    next_position = current_position + move
    is_box = warehouse[*next_position] == 'O'
    is_empty = warehouse[*next_position] == '.'
    if is_box:
        new_box_position = next_position + move
        box_q = [new_box_position]
        # If the next space isn't empty or a wall, it's a box.
        while warehouse[*new_box_position] not in ".#":
            new_box_position = new_box_position + move
            box_q.append(new_box_position)
        # If the last queued space is a wall, then there's no space to push.
        if box_q and warehouse[*box_q[-1]] == '#': continue
        # Otherwise, push all the queued boxes forward one space.
        while box_q:
            warehouse[*(box_q.pop())] = 'O'
        warehouse[*next_position] = '@'
        warehouse[*current_position] = '.'
        current_position = next_position
    elif is_empty:
        warehouse[*next_position] = '@'
        warehouse[*current_position] = '.'
        current_position = next_position

boxes = np.argwhere(warehouse == 'O').tolist()
gps_sum = 0
for box in boxes:
    x, y = box
    gps_sum += 100 * x + y

print(f'PART 1\tGPS coordinates sum: {gps_sum}')
