"""
Advent of Code 2024
Day 6: Guard Gallivant

Part 1 simulates the guard's movement under the implicit assumption that she 
will eventually leave the lab. It updates a bit mask of tiles that the guard 
visits along her path.

Part 2 is a brute force solution in that it iteratively places one obstacle, 
simulates the guard's movement as in Part 1, and detects whether she leaves 
the lab or gets caught in a cycle. The search space is shrunk by placing 
obstacles only on tiles that the guard visits in Part 1. That gives ~5,000 
paths to simulate instead of the ~17,000 if we tried placing an obstacle 
in every tile in the grid. On my machine, this runs in about ~20 s.

Note: If trying to gauge the progress in Part 2, cast the zipped indexes to a 
list and wrap it with tqdm.
"""

import numpy as np


def traverse(start, direction, dims):
    """
    Traverse the lab. This assumes that the guard is guaranteed to 
    eventually move out of bounds given the obstacle placement.

    Returns nothing but modifies the visited matrix.
    """
    guard_location = start
    while is_in_bounds(guard_location, dims):
        visited[guard_location] = True
        next_location = move(guard_location, facing[direction])
        # Turn 90 degrees to the right for as long as the guard would move 
        # into an obstacle.
        while is_in_bounds(next_location, dims) and is_obstacle[next_location]:
            direction = (direction + 1) % 4
            next_location = move(guard_location, facing[direction])
        guard_location = next_location


def traverse_with_cycles(start, direction, dims):
    """
    Traverse the lab but with cycle detection.

    Modifies the visited matrix and returns True if a cycle is detected.
    """
    guard_location = start
    is_potential_cycle = False
    while is_in_bounds(guard_location, dims):
        # A cycle is potentially detected if the guard arrives at a tile 
        # that she's already visited.
        if visited[guard_location] and not is_potential_cycle:
            is_potential_cycle = True
            cycle_start = guard_location
        # Since the guard's path can cross itself, if she moves from a 
        # visited tile to an unvisited tile, then she cannot be in a cycle.
        elif not visited[guard_location] and is_potential_cycle:
            is_potential_cycle = False
        elif is_potential_cycle and guard_location == cycle_start:
            return True
        # If no cycle is detected, continue the traversal.
        visited[guard_location] = True
        next_location = move(guard_location, facing[direction])
        while is_in_bounds(next_location, dims) and is_obstacle[next_location]:
            direction = (direction + 1) % 4
            next_location = move(guard_location, facing[direction])
        guard_location = next_location
    
    return False


def is_in_bounds(location, dims):
    x, y = location
    x_max, y_max = dims
    return 0 <= x < x_max and 0 <= y < y_max


def move(current_location, direction):
    x, y = current_location
    # The Cartesian coordinate (x,y) is actually operated on as (y,x) since
    # NumPy is row major.
    if direction == '^':
        return x - 1, y
    elif direction == '>':
        return x, y + 1
    elif direction == 'v':
        return x + 1, y
    elif direction == '<':
        return x, y - 1


with open("../_tests/day06.txt") as f:
    patrol_map = f.read().splitlines()
    patrol_map = np.array([list(line) for line in patrol_map])
    dims = patrol_map.shape

# Find the 2D index of the guard's starting location.
start_location = np.argmax(patrol_map == '^')
start_location = np.unravel_index(start_location, dims)

# Create masks of where obstacles are and where the guard visits.
is_obstacle = patrol_map == '#'
visited = np.zeros(dims, dtype='bool')

# The guard is initially facing up and will first try to move that way. 
# Movement direction is enumerated by 0, 1, 2, or 3. This mapping is purely 
# for readability and my understanding.
facing = {0: '^', 1: '>', 2: 'v', 3: '<'}
start_direction = 0    

# PART 1.
traverse(start_location, start_direction, dims=dims)
print(f'PART 1\tNumber of distinct visited tiles: {visited.sum()}')

# PART 2.
valid_obstacle_count = 0
visited_indexes = zip(*np.where(visited))
for i, j in visited_indexes:
    # An obstacle cannot be placed in the guard's starting location.
    if (i, j) == start_location:
        continue
    # Reset the visited mask.
    visited = np.zeros(dims, dtype='bool')
    # Place the obstacle.
    is_obstacle[i,j] = True
    # Try traversing the lab; break if the guard gets caught in a loop.
    cycle_detected = traverse_with_cycles(start_location, start_direction, dims=dims)
    if cycle_detected:
        valid_obstacle_count += 1
    # Reset the placed obstacle for the next iteration.
    is_obstacle[i,j] = False

print(f'PART 2\tNumber of valid obstacle placements: {valid_obstacle_count}')
