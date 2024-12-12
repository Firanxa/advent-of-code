"""
Advent of Code 2015
Day 11: Corporate Policy

I opted for a class-based solution just for some practice writing Python 
classes. I think it generalizes well because the rules and password 
requirements can be easily set within the class definition. (Not that any of
that was required for this problem, but still - good practice).

Setting the next password works by incrementing the order, i.e., the ASCII 
value, of the rightmost character. If this exceeds the order of the last 
permitted character, 'z', then roll it over to 'a' and increment the order of 
the next character to the left. Repeat this process for that character if this 
causes another rollover, and so forth.

I could've improved this process by skipping the forbidden characters 'i', 
'o', and 'l', but I can live with the performance hit. This also means that 
the time to completion will vary with your input!

When checking if a password is valid, I used `itertools.groupby` for the first 
time. It generates groups from an iterable's items in order according to a 
key, which by default is the identity function. Here, it yields each character 
in a string with a list of the consecutive appearances of that character 
until the next break. For example, "aabcdd" would yield

    'a' => ['a', 'a'],
    'b' => ['b'],
    'c' => ['c'],
    'd' => ['d', 'd']
"""

from itertools import groupby


class PasswordGenerator:
    required_password_length = 8
    start_char = 'a'
    end_char = 'z'

    def __init__(self, password):
        if not password.isalpha() or password.lower() != password:
            raise ValueError("Password must be lowercase letters only.")
        if len(password) != self.required_password_length:
            raise ValueError("Password must be exactly eight letters.")
        self.password = password
        self.has_valid_password = self.is_valid(self.password)

    def set_next_password(self):
        ords = list(map(ord, self.password))
        i = self.required_password_length - 1
        # Increment the password starting from the rightmost letter.
        ords[i] += 1
        # Rolling over from 'z' to 'a' causes the next letter to the left to 
        # increment. Repeat this process if the increment causes another 
        # rollover.
        while ords[i] > ord(self.end_char):
            ords[i] = ord(self.start_char)
            ords[i-1] += 1
            i -= 1

        self.password = "".join(map(chr, ords))
        self.has_valid_password = self.is_valid(self.password)

    def is_valid(self, password):
        # Rule 1.
        has_straight = False
        min_length = 3
        for i in range(self.required_password_length - min_length):
            ords = list(map(ord, password[i:i+min_length]))
            # This line could be generalized for a straight of arbitrary 
            # minimum length.
            if ords[0] == ords[1] - 1 == ords[2] - 2:
                has_straight = True
                break

        # Rule 2.
        contains_iol = any([letter in password for letter in "iol"])

        # Rule 3.
        pairs = []
        for _, group in groupby(password):
            # `groupby` with `key=None` generates a break (a new group) every 
            # time the key value changes, i.e., on a new character.
            grouped_letters = ''.join(group)
            if len(grouped_letters) == 2:
                pairs.append(grouped_letters)
        unique_pairs = set(pairs)
        has_two_pairs = len(unique_pairs) >= 2

        return (has_straight and not contains_iol and has_two_pairs)


with open("../_tests/day11.txt") as f:
    current_password = f.read().strip()

# PART 1.
pg = PasswordGenerator(current_password)
while not pg.has_valid_password:
    pg.set_next_password()

print(f'PART 1\tNext password is: {pg.password}')

# PART 2.
pg.set_next_password()
while not pg.has_valid_password:
    pg.set_next_password()

print(f'PART 2\tNext password is: {pg.password}')
