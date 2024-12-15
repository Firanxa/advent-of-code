"""
Advent of Code 2024
Day 13: Claw Contraption

This problem reduces to linear systems of two equations in two unknowns, and 
we have to determine which systems have integer solutions. Let `a` be the 
number of times you push button A, `b` the number of times you push button B. 
Given the prize position `p` = (x_p, x_p), we seek (a, b) such that

    a * x_a + b * x_b = x_p
    a * y_a + b * y_b = y_p

where (x_i, y_i) is the movement for each push of button i. We can solve this 
algebraically, then check if (a, b) are both integers.
"""

with open("../_tests/day13.txt") as f:
    lines = f.read().splitlines()

parse = lambda s: int(''.join([x for x in s if x.isdigit()]))

tol = 1e-3
tokens_1 = 0
tokens_2 = 0
for i in range(0, len(lines), 4):
    # A button.
    a_line = lines[i].split()
    ax, ay = parse(a_line[2]), parse(a_line[3])

    # B button.
    b_line = lines[i+1].split()
    bx, by = parse(b_line[2]), parse(b_line[3])
    
    # Prize position.
    prize_line = lines[i+2].split()
    px, py = parse(prize_line[1]), parse(prize_line[2])

    # PART 1.
    a = (py - px * by / bx) / (ay - ax * by / bx)
    b = (px - a * ax) / bx
    
    # Integer solutions might be off of a whole number within tolerance due to
    # floating point error.
    if abs(a - round(a)) < tol and abs(b - round(b)) < tol:
        tokens_1 += 3 * a + b

    # PART 2.
    px += 10000000000000
    py += 10000000000000
    a = (py - px * by / bx) / (ay - ax * by / bx)
    b = (px - a * ax) / bx
    
    if abs(a - round(a)) < tol and abs(b - round(b)) < tol:
        tokens_2 += 3 * a + b

print(f'Number of tokens: {int(tokens_1)}')
print(f'Number of tokens: {int(tokens_2)}')
