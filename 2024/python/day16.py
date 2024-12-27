"""
Advent of Code 2024
Day 16: Reindeer Maze

Both parts require just Dijkstra's algorithm but with a clever kind of graph 
to be able to include turn costs. I define a state according to the (NumPy) 
axis that the reindeer is facing within the maze: North-south (axis 0) or 
east-west (axis 1). Then every tile in the maze contributes two nodes: One for 
if the reindeer is passing through it north-south, one if east-west. The cost 
of moving from one tile to the next along the same axis is 1, and it's 1001 
to move and change orientation from one axis to the other. Dijkstra's 
algorithm quickly gives the shortest, i.e., lowest-scoring, path with these 
edge weights.
"""

import numpy as np
import networkx as nx


def get_neighbors(x, y, x_max, y_max):
    """Returns a list of points 4-adjacent to the point (x, y)."""
    neighbors = []
    if y < y_max - 1:
        neighbors.append((x, y + 1))
    if x < x_max - 1:
        neighbors.append((x + 1, y))
    if y > 0:
        neighbors.append((x, y - 1))
    if x > 0:
        neighbors.append((x - 1, y))
    
    return neighbors


with open("../_tests/day16.txt") as f:
    maze = np.array([list(line) for line in f.read().splitlines()])
    dims = maze.shape

# PART 1.
G = nx.DiGraph()
for tile in np.ndindex(dims):
    # Skip the maze walls.
    if maze[*tile] == '#': continue
    # Add the end tile as nodes with only in-edges.
    elif maze[*tile] == 'E':
        G.add_node((tile, 0))
        G.add_node((tile, 1))
    # All tiles contribute two nodes, one for each axis that the reindeer can 
    # be passing through it along.
    else:
        G.add_node((tile, 0))
        G.add_node((tile, 1))
        neighbors = get_neighbors(*tile, *dims)
        neighbors = [x for x in neighbors if maze[*x] in ".E"]
        for neighbor in neighbors:
            dx = abs(tile[0] - neighbor[0])
            dy = abs(tile[1] - neighbor[1])
            # No change in axis 0, therefore moving EW.
            if dx == 0:
                G.add_edge((tile, 1), (neighbor, 1), weight=1)
                G.add_edge((tile, 0), (neighbor, 1), weight=1001)
            # No chnage in axis 1, therefore moving NS.
            elif dy == 0:
                G.add_edge((tile, 0), (neighbor, 0), weight=1)
                G.add_edge((tile, 1), (neighbor, 0), weight=1001)

# The maze starts facing along the EW axis.
start = np.argmax(maze == 'S')
start = np.unravel_index(start, dims)
start = (start, 1)

# The end tile can be reached from either the NS or EW axes. The overall 
# shortest path is the shorter of the two shortest paths ending along each 
# axis.
end = np.argmax(maze == 'E')
end = np.unravel_index(end, dims)
path_lengths = []
for end_dir in [0, 1]:
    path_length = nx.shortest_path_length(G, start, (end, end_dir), weight="weight")
    path_lengths.append(path_length)
end_dir = path_lengths.index(min(path_lengths))

print(f'PART 1\tLowest possible score: {path_lengths[end_dir]}')

# PART 2.
paths = nx.all_shortest_paths(G, start, (end, end_dir), weight="weight")
tiles = set(tile for path in paths for tile, _ in path)

print(f'PART 2\tNumber of tiles: {len(tiles)}')
