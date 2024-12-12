"""
Advent of Code 2015
Day 12: JSAbacusFramework.io

Regex made short work of Part 1; the heavy lifting was in Part 2.

Part 2 takes advantage of a JSON object's tree-like structure by recursively 
"deleting" every object with a red-valued property. (Really, it replaces the 
object with `None` rather than delete it). The edited JSON is dumped back to 
text, then the solution to Part 1 can be applied.

This does align with the problem description that we should ignore "red" 
objects; it never explicitly says to delete them, nor does the solution 
require it. Doing so would require pointers to recursively alter the JSON in 
place.
"""

import json
import re


def get_nums_sum(text):
    nums = re.findall(r'-?\d+\.?\d*', text)
    total_sum = sum(map(int, nums))
    return total_sum


def delete_red_children(d):
    # Arrays should be checked for objects with any red-valued proeprty, 
    # although "red" as an array element has no effect.
    if isinstance(d, list):
        d = [delete_red_children(item) for item in d]
    elif isinstance(d, dict):
        # For the value v of each property k...
        for k, v in list(d.items()):
            # If v is an array, check as above.
            if isinstance(v, list):
                d[k] = [delete_red_children(item) for item in v]
            # If v is another object, recurse into it.
            elif isinstance(v, dict):
                d[k] = delete_red_children(v)
            # If v is "red", mark this object to be ignored.
            if v == "red":
                d = None
                break

    return d


with open("../_tests/day12.txt") as f:
    doc = f.read().strip()

# PART 1.
print(f'PART 1\tSum of all numbers: {get_nums_sum(doc)}')

# PART 2.
data = json.loads(doc)
red_filtered_data = delete_red_children(data)
dump = json.dumps(red_filtered_data)
print(f'PART 2\tSum of all numbers (minus "red" objects): {get_nums_sum(dump)}')
