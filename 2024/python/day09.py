"""
Advent of Code 2024
Day 9: Disk Fragmenter

Part 2 drove me nuts. It's the only part so far that I've solved past the 
24-hour mark.

For both parts, I parse the disk map to a list of files and expand it to a 
list of blocks for Part 1. This made swapping file blocks in the right to 
free blocks in the left straightforward. But for Part 2, I tried moving whole 
files within the original list and struggled trying to move and resize free 
space with each swap.

In the end, I moved files block-by-block by tracking every file and free 
space's starting index in the original list of blocks. I used a min heap to 
track the size of free spaces prioritized by their position. This way, new 
space freed in the right and space shrunk in the left could be queued with 
minimal overhead.

I think this is a step toward the most efficient implementation; as is, Part 1 
runs instantly, and Part 2 takes ~20 s. I think I could improve it by using a 
a list of min heaps, one for each file size 1..9. Then for each file, we would 
instantly know which spaces, if any, it can move into and select the one with 
the highest priority.
"""

import heapq
from collections import namedtuple


File = namedtuple("File", ["id", "size", "drive_index"])


def compute_checksum(blocks):
    """
    Computes the checksum of a list of blocks where each block records the ID 
    of the file written in it.
    """
    return sum(i * file_id for i, file_id in enumerate(blocks) if file_id != -1)


def disk_to_blocks(hd):
    """Expands a list of files to a list of blocks."""
    disk_size = sum(file.size for file in hd)    
    blocks = [None] * disk_size
    index = 0
    for file in hd:
        for i in range(index, index + file.size):
            blocks[i] = file.id
        index += file.size

    return blocks


with open("../_tests/day09.txt") as f:
    disk_map = f.read()

# Create a list of files according to the disk map's specifications.
hd = []
file_id = 0
file_q = []
space_pq = []
index = 0
for i, digit in enumerate(disk_map):
    file_size = int(digit)
    if i % 2 == 0:
        file = File(file_id, file_size, index)
        # Stack the files so that they can be later moved from right to left.
        file_q.append(file)
        file_id += 1
    else:
        file = File(-1, file_size, index)
        # Keep a min heap of the free spaces to prioritize the leftmost space.
        space_pq.append((index, file_size))
    index += file_size
    hd.append(file)

# PART 1.
blocks = disk_to_blocks(hd)
left = 0
right = len(blocks) - 1
while left < right:
    while blocks[left] != -1:
        left += 1
    while not blocks[right] >= 0:
        right -= 1
    if left >= right:
        break
    blocks[left], blocks[right] = blocks[right], blocks[left]

checksum = compute_checksum(blocks)
print(f'PART 1\tChecksum: {checksum}')

# PART 2.
heapq.heapify(space_pq)
blocks_compact = disk_to_blocks(hd)
while file_q:
    file = file_q.pop()
    storage = []
    while space_pq:
        index, free_space = heapq.heappop(space_pq)
        size_diff = free_space - file.size
        if index <= file.drive_index and size_diff >= 0:
            # Write the file to the leftmost available free space.
            for k in range(index, index + file.size):
                blocks_compact[k] = file.id
            # Free the file's original location.
            for k in range(file.drive_index, file.drive_index + file.size):
                blocks_compact[k] = -1
            # Shrink the free space if the file doesn't fill it.
            if size_diff > 0:
                storage.append((index + file.size, size_diff))
            break
        else:
            storage.append((index, free_space))
    # Push all invalid free spaces back into the heap and heapify.
    if storage:
        space_pq += storage
        storage = []
        heapq.heapify(space_pq)

checksum = compute_checksum(blocks_compact)
print(f'PART 2\tChecksum: {checksum}')
