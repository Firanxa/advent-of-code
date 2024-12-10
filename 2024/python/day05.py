"""
Advent of Code 2024
Day 5: Print Queue

This one is easy with custom sorting. The tricky part, for me, was getting the 
callable in `cmp_to_key` to behave correctly. Mine is probably not the most 
efficient implementation, since each comparison performs a linear scan of a 
list of valid pages, but I'm happy with it nonetheless. (This program runs
fast on the given input anyway).

Another approach would be to treat the pages as nodes in a directed graph, 
with the page ordering rules the directed edges to other pages. Then assessing 
whether an update is valid amounts to checking whether there is a directed 
edge from page to page in the update's listed order.

I got the right answer to Part 1 by this approach, but Part 2 stumped me; I 
pursued the sorting solution instead. I found out later that there does exist 
a sort for this situation: Topological sorting, which NetworkX implements.
"""

import networkx as nx
from functools import cmp_to_key
from itertools import pairwise


def order_pages(page_before, page_after):
    """Custom comparator for whether one page can appear before another."""
    valid_pages_after = rules.get(page_before, [])
    if page_after not in valid_pages_after:
        return 1
    elif page_before == page_after:
        return 0
    else:
        return -1


def is_valid(update, G):
    """Returns whether a directed path exists through the given page order."""
    return all([G.has_edge(u, v) for u, v in pairwise(update)])


with open("../_tests/day05.txt") as f:
    text = f.read().splitlines()
    rules = {}
    updates = []
    reading_rules = True
    for line in text:
        # The rules and updates blocks are separated by a blank line. This is 
        # a hacky way to parse them separately but in one pass.
        if not line:
            reading_rules = False
            continue
        # Map each page number to a list of valid page numbers that can 
        # follow it.
        if reading_rules:
            page_before, page_after = tuple(map(int, line.split('|')))
            rules[page_before] = rules.get(page_before, []) + [page_after]
        else:
            updates.append(list(map(int, line.split(','))))

# Original solution by sorting with a custom comparator.
middle_page_number_sum = 0
corrected_middle_page_number_sum = 0
for update in updates:
    n = len(update)
    sorted_update = sorted(update, key=cmp_to_key(order_pages))
    # PART 1.
    if update == sorted_update:
        middle_page_number = update[n // 2]
        middle_page_number_sum += middle_page_number
    # PART 2.
    else:
        corrected_middle_page_number = sorted_update[n // 2]
        corrected_middle_page_number_sum += corrected_middle_page_number

print("Solved by sorting with a custom comparator:")
print(f'PART 1\tPage number sum: {middle_page_number_sum}')
print(f'PART 2\tCorrected page number sum: {corrected_middle_page_number_sum}')

# Alternate solution treating the rules as a directed acyclic graph.
alt_ans_1 = 0
alt_ans_2 = 0
G = nx.DiGraph(rules)
for update in updates:
    n = len(update)
    if is_valid(update, G):
        middle_page_number = update[n // 2]
        alt_ans_1 += middle_page_number
    else:
        H = G.subgraph(update)
        sorted_update = list(nx.topological_sort(H))
        corrected_middle_page_number = sorted_update[n // 2]
        alt_ans_2 += corrected_middle_page_number

assert alt_ans_1 == middle_page_number_sum
assert alt_ans_2 == corrected_middle_page_number_sum

print("\nSolved with a DAG:")
print(f'PART 1\tPage number sum: {alt_ans_1}')
print(f'PART 2\tCorrected page number sum: {alt_ans_2}')
