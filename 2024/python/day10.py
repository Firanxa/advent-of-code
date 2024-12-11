"""
Advent of Code 2024
Day 10: Hoof It

Part 1 is (what should have been) a simple DFS. I spent a lot of time 
not realizing that I forgot to pass an empty list to `paths=[]` for the DFS 
initiated at each trailhead. But getting the DFS right meant that Part 2
followed immediately from the work done for Part 1.
"""

import numpy as np


def find_paths(grid, current_path=[(0, 0)], paths=[]):
    """
    DFS to find all peaks reachable from a given trailhead. Input requires a 
    list with one element, the starting coordinates of the trailhead.

    Returns a list of lists of coordinates, where each list is a path from the 
    trailhead to a peak.
    """
    assert current_path, "Search requires a list with starting point [(x, y)]."
    if len(current_path) == 1:
        start = current_path[0]
        assert grid[start] == 0, "Search must start at a trailhead."
    
    # Can go up, right, left, or down from current position (x, y).
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    x, y = current_path[-1]
    x_max, y_max = grid.shape
    for (dx, dy) in directions:
        new_x = x + dx
        new_y = y + dy
        # Check if in bounds.
        if (new_x < 0 or new_x >= x_max) or (new_y < 0 or new_y >= y_max):
            continue
        # Check if next point follows the trail.
        if grid[new_x,new_y] != grid[x,y] + 1:
            continue
        # Check if next point has already been visited.
        if (new_x, new_y) in current_path:
            continue
        # Otherwise, move to next point.
        current_path_copy = current_path.copy()
        current_path_copy.append((new_x, new_y))
        # Paths conclude at a peak.
        if grid[new_x,new_y] == 9:
            paths.append(current_path_copy)
        # Recurse.
        find_paths(grid, current_path=current_path_copy, paths=paths)
    
    return paths


def trailhead_score(paths):
    """
    Calculates trailhead score as the number of unique peaks reached from a 
    trailhead. Throws an error if the paths do not have the same trailhead.
    """
    assert len({path[0] for path in paths}) == 1, "Check trailhead"
    return len({path[-1] for path in paths})


def trailhead_rating(paths):
    """
    Returns the number of paths that originate from the same trailhead. Throws 
    an error if the paths do not have the same trailhead.
    """
    assert len({path[0] for path in paths}) == 1, "Check trailhead"
    return len(paths)


with open("../_tests/day10.txt") as f:
    topo_map = f.read().splitlines()
    topo_map = np.array([list(line) for line in topo_map], dtype='int')

trailheads = [tuple(coord) for coord in np.argwhere(topo_map == 0).tolist()]
score_sum = 0
rating_sum = 0
for trailhead in trailheads:
    current_path = [trailhead]
    paths = find_paths(topo_map, current_path, paths=[])
    # PART 1.
    score_sum += trailhead_score(paths)
    # PART 2.
    rating_sum += trailhead_rating(paths)
    
print(f'PART 1\tSum of trailhead scores: {score_sum}')
print(f'PART 2\tSum of trailhead ratings: {rating_sum}')
