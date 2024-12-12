"""
Advent of Code 2015
Day 2: I Was Told There Would Be No Math

Another straightforward problem to start.
"""

with open("../_tests/day02.txt") as f:
    dims_list = f.readlines()

total_paper = 0
total_ribbon = 0
for dims in dims_list:
    dims = dims.split('x')
    l, w, h = map(int, dims)

    # PART 1.
    side_areas = (l * w, w * h, h * l)
    sq_ft = 2 * sum(side_areas) + min(side_areas)
    total_paper += sq_ft

    # PART 2.
    semiperims = (l + w, w + h, h + l)
    min_perim = 2 * min(semiperims)
    vol = l * w * h
    total_ribbon += min_perim + vol

print(f'PART 1\tTotal sq. ft. of wrapping paper: {total_paper}')
print(f'PART 2\tTotal ft. of ribbon: {total_ribbon}')
