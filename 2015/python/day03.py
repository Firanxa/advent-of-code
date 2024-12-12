"""
Advent of Code 2015
Day 3: Perfectly Spherical Houses in a Vacuum

Two helpful facts about dicts that I took advantage of in this problem:
    1) Use `get` to check if a key is present then operate on its value. This 
    is less clunky than an if/else block for simple operations.
    2) Dicts are (essentially) passed by reference. This means functions can 
    read and modify a dict as if it were a global variable without having to 
    declare it as one.
"""

def deliver_and_move(current_coord, visited_coords, direction):
    visited_coords[current_coord] = visited_coords.get(current_coord, 0) + 1
    new_coord = move(*current_coord, direction)
    visited_coords[new_coord] = visited_coords.get(new_coord, 0) + 1

    return new_coord


def move(x, y, direction):
    if direction == '^':
        y += 1
    elif direction == '>':
        x += 1
    elif direction == 'v':
        y -= 1
    else:
        x -= 1

    return x, y


with open("../_tests/day03.txt") as f:
    directions = f.read()

# PART 1.
current_coord = (0, 0)
visited_coords = {}
for direction in directions:
    current_coord = deliver_and_move(current_coord, visited_coords, direction)

print(f'PART 1\tHouses receiving presents: {len(visited_coords)}')

# PART 2.
santa_coord = (0, 0)
robot_coord = (0, 0)
visited_coords = {}
for i, direction in enumerate(directions):
    if i % 2 == 0:
        santa_coord = deliver_and_move(santa_coord, visited_coords, direction)
    else:
        robot_coord = deliver_and_move(robot_coord, visited_coords, direction)

print(f'PART 2\tHouses receiving presents: {len(visited_coords)}')
