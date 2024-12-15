"""
Advent of Code 2024
Day 12: Garden Groups

I use a flood fill algorithm for Part 1. Since plants are separated into 
different contiguous plots, I enumerate plots as they're discovered and 
"color" each point in the map grid with the unique ID of the plot it belongs 
to.

I have ideas for Part 2 but am still stumped on how to implement them... A 
couple things I've tried that I cannot get to work on the test input:

    - Count the number of corners in each plot. Every corner means a 
    horizontal side becomes a vertical side, and vice versa.
    - Count the number of horizontal (or vertical) sides in each plot and 
    multiply by 2. There must be one horizontal side for every vertical side 
    in order to close the plot.
"""

import numpy as np
from collections import deque


def get_neighbors(x, y, x_max, y_max):
    """
    Returns a list of points 4-adjacent to the point (x, y). The ordering is 
    [top, left, bottom, right]. A neighbor is None if (x, y) is on the map's 
    border in that direction.
    """
    neighbors = [None] * 4
    if y < y_max - 1:
        neighbors[0] = (x, y + 1)
    if x < x_max - 1:
        neighbors[1] = (x + 1, y)
    if y > 0:
        neighbors[2] = (x, y - 1)
    if x > 0:
        neighbors[3] = (x - 1, y)
    
    return neighbors


with open("../_tests/day12.txt") as f:
    plant_map = f.read().splitlines()
    plant_map = np.array([list(line) for line in plant_map])
    dims = plant_map.shape

areas = {}
perimeters = {}
plants = {}
plot_id = 0

# Initialize the fill at any point.
start = (0, 0)
farm_map = np.zeros(dims, dtype='int')
visited = np.zeros(dims, dtype='bool')

# Maintain queues for filling each plot.
q_current_plot = deque()
q_to_visit = deque()
q_to_visit.append(start)

while q_to_visit:
    seed = q_to_visit.popleft()
    if visited[seed]: continue
    
    # The current point determines what plant and plot ID to "color" this 
    # region with.
    current_plant = plant_map[seed]
    plants[plot_id] = current_plant
    q_current_plot.append(seed)

    while q_current_plot:
        point = q_current_plot.popleft()
        if visited[point]: continue
        if plant_map[point] == current_plant:
            neighbors = get_neighbors(*point, *dims)
            # Count how many of this point's sides are map borders.
            border_count = sum(not neighbor for neighbor in neighbors)
            # Count how many of this point's neighbors are in other plots.
            boundary_count = sum(
                plant_map[neighbor] != current_plant
                for neighbor in neighbors if neighbor)

            # Update the area and perimeter counts.
            areas[plot_id] = areas.get(plot_id, 0) + 1
            perimeters[plot_id] = perimeters.get(plot_id, 0) + \
                border_count + boundary_count
            
            # "Color" the map.
            farm_map[point] = plot_id

            # Enqueue neighboring points.
            for neighbor in neighbors:
                if neighbor:
                    q_current_plot.append(neighbor)

            # This point is done.
            visited[point] = True
        else:
            q_to_visit.append(point)
    
    plot_id += 1

# PART 1.
total_price = 0
for key in areas.keys():
    total_price += areas[key] * perimeters[key]

print(f'PART 1\tTotal price of fencing: {total_price}')
