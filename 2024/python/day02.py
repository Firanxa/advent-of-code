"""
Advent of Code 2024
Day 2: Red-Nosed Reports

Both safety rules can be checked via the differences between consecutive
levels in each report. `itertools.pairwise` handles this cleanly with NumPy.

My solution to Part 2 is technically brute forced, but it works well. If an 
unsafe report is of length p, then it checks the safety of at most p reports 
with the i-th level removed.
"""

import numpy as np
from itertools import pairwise


def check_safety(report, with_dampening=False):
    """
    Checks if a report passes the two safety rules:
        1. The levels in the report are strictly monotonic;
        2. The differences between consecutive levels are in the range [1,3].
    
    If checked with dampening, then a report is tolerably safe if it passes 
    the two rules after removing exactly one level from an otherwise unsafe 
    report.
    """
    def is_strictly_monotonic(x_diffs):
        # A sequence is strictly monotonic if the differences of consecutive 
        # elements are all of the same sign.
        return np.all(x_diffs > 0) or np.all(x_diffs < 0)

    def is_within_range(x_diffs):
        abs_x_diffs = np.abs(x_diffs)
        return np.all(1 <= abs_x_diffs) and np.all(abs_x_diffs <= 3)

    def passes_rules(x):
        diffs = np.array([b - a for a, b in pairwise(x)])
        return is_strictly_monotonic(diffs) and is_within_range(diffs)

    is_safe = passes_rules(report)
    # Runs only for reports in Part 2 and if is_safe = False for that report.
    if with_dampening and not is_safe:
        n = len(report)
        for i in range(n):
            report_minus_i = report[np.arange(n) != i]
            if passes_rules(report_minus_i):
                is_safe = True
                break
    
    return is_safe


with open("../_tests/day02.txt") as f:
    reports = f.readlines()

safe_report_count = 0
tolerable_report_count = 0
for report in reports:
    report = np.array(report.split(), dtype='int')
    # PART 1.
    safe_report_count += check_safety(report)
    # PART 2.
    tolerable_report_count += check_safety(report, with_dampening=True)

print(f'PART 1\tNumber of safe reports: {safe_report_count}')
print(f'PART 2\tNumber of tolerable reports: {tolerable_report_count}')
