"""
Advent of Code 2015
Day 5: Doesn't He Have Intern-Elves For This?

I found the simplest way to do this was to write a boolean function for each
rule, then check what every string evaluates to for each rule set.
"""

# Rules for PART 1.
def has_three_vowels(s):
    vowels = "aeiou"
    vowel_counts = {vowel: s.count(vowel) for vowel in vowels}
    return sum(vowel_counts.values()) >= 3


def has_double_char(s):
    for i in range(1, len(s)):
        if s[i] == s[i-1]:
            return True
    return False


def contains_special_seq(s):
    special_seqs = ["ab", "cd", "pq", "xy"]
    for seq in special_seqs:
        if seq in s:
            return True
    return False


def satisfies_ruleset_1(s):
    return (has_three_vowels(s) and has_double_char(s) and
            not contains_special_seq(s))


# Rules for PART 2.
def contains_doublet_pair(s):
    n = len(s)
    for i in range(1, n):
        doublet = s[i-1] + s[i]
        for j in range(i + 2, n):
            next_doublet = s[j-1] + s[j]
            if doublet == next_doublet:
                return True
    return False


def contains_sandwich(s):
    for i in range(2, len(s)):
        if s[i] == s[i-2]:
            return True
    return False


def satisfies_ruleset_2(s):
    return (contains_doublet_pair(s) and contains_sandwich(s))


with open("../_tests/day05.txt") as f:
    strings = f.read().splitlines()

# PART 1.
nice_strings_1 = sum(satisfies_ruleset_1(string) for string in strings)
print(f'PART 1\tNice string count with ruleset 1: {nice_strings_1}')

# PART 2.
nice_strings_2 = sum(satisfies_ruleset_2(string) for string in strings)
print(f'PART 2\tNice string count with ruleset 2: {nice_strings_2}')
