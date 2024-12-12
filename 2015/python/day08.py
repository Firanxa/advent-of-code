"""
Advent of Code 2015
Day 8: Matchsticks

I discovered the `eval` function, which makes Part 1 a one-liner. For Part 2,
I initially tried to build the new string through pattern matching, but it 
ultimately wasn't worth the effort to get the escape characters printing 
properly. It was much simpler to just count how many new characters would be 
added for each special character in the new encoding.
"""

with open("../_tests/day08.txt") as f:
    strings = f.read().splitlines()

char_difference = 0
new_char_difference = 0
for string in strings:
    # PART 1.
    char_difference += len(string) - len(eval(string))
    # PART 2.
    added_char_count = 2 + string.count('"') + string.count('\\')
    new_char_difference += added_char_count

print(f'PART 1\tChar count difference between representations: {char_difference}')
print(f'PART 2\tChar count difference after encoding: {new_char_difference}')
