"""
Advent of Code 2015
Day 14: Reindeer Olympics

I initially solved Part 1 by calculating how far each reindeer travels in 
T = 2503 s, then taking the maximum distance. But Part 2 requires knowing 
where each reindeer is at each second, so I implemented a "simulation" of the 
race that answers both parts.
"""

import numpy as np
from collections import namedtuple


Reindeer = namedtuple("Reindeer", ["name", "speed", "duration", "rest_length"])


def trajectory(T, reindeer):
    x = np.zeros(T)
    t = 0
    time_remaining = reindeer.duration
    is_moving = True
    current_position = 0
    while t < T:
        # This loop represents both the flight and rest cycles. It will break
        # once the total time T elapses, even if a cycle isn't complete.
        while time_remaining > 0 and t < T:
            if is_moving:
                current_position += reindeer.speed
            x[t] = current_position
            t += 1
            time_remaining -= 1
        if is_moving:
            time_remaining = reindeer.rest_length
        else:
            time_remaining = reindeer.duration
        # Alternate between flight and rest cycles.
        is_moving = not is_moving

    return x


with open("../_tests/day14.txt") as f:
    text = f.readlines()

reindeer_list = []
for line in text:
    split_line = line.split()
    name = split_line[0]
    speed = int(split_line[3])
    duration = int(split_line[6])
    rest_length = int(split_line[-2])
    reindeer_list.append(Reindeer(name, speed, duration, rest_length))

# PART 1.
n = len(reindeer_list)
T = 1000
# T = 2503

positions = np.zeros((n, T), dtype="int")
for i, reindeer in enumerate(reindeer_list):
    positions[i] = trajectory(T, reindeer)

winner = reindeer_list[np.argmax(positions[:,-1])].name
distance = positions[:,-1].max()

print(f'PART 1\t{winner} is the winner, traveling: {distance} km')

# PART 2.
points = np.zeros(n, dtype="int")
for t in range(T):
    current_positions = positions[:,t]
    # If multiple reindeer are tired for the lead, they each get a point.
    in_the_lead = np.argwhere(current_positions == current_positions.max())
    points[in_the_lead] += 1

winner = reindeer_list[np.argmax(points)].name
total_points = points.max()

print(f'PART 2\t{winner} is the winner, with: {total_points} points')
