"""
Advent of Code 2015
Day 10: Elves Look, Elves Say

The tricky part was remembering the edge cases when the entire sequence is
the same digit and when the last digit differs from the the penultimate one.

The sequences blow up in length very quickly, so Part 2 runs noticeably 
slower than Part 1 even though it's only 10 iterations more. I wonder if 
there's a more space-efficient way to store successive sequences.
"""

def look_and_say(seq):
    digit_count_list = []
    current_digit = seq[0]
    current_count = 0
    n = len(seq)

    for i, digit in enumerate(seq):
        if digit == current_digit:
            current_count += 1
        else:
            digit_count_list.append((current_digit, current_count))
            current_digit = digit
            current_count = 1
        # Handles the two edge cases described above.
        if i == n - 1:
            digit_count_list.append((current_digit, current_count))

    new_seq = ""
    for digit, count in digit_count_list:
        new_seq += f'{count}{digit}'

    return new_seq


def solve_day10(seq, K):
    for _ in range(K):
        seq = look_and_say(seq)
    return len(seq)


with open("../_tests/day10.txt") as f:
    seq = f.read().strip()

# PART 1.
K = 40
print(f'PART 1\tSequence length after {K} iterations: {solve_day10(seq, K)}')

# PART 2.
K = 50
print(f'PART 2\tSequence length after {K} iterations: {solve_day10(seq, K)}')
