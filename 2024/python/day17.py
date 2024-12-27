"""
Advent of Code 2024
Day 17: Chronospatial Computer

I like the object-oriented approach for Part 1. It makes processing 
instructions look natural.

For Part 2, I tried the brute-force solution of initializing register A to 0, 
processing the instructions as in Part 1, and comparing the output values to 
the program; as soon as they don't match, break and increment the register. 
This got me nowhere (and I wasn't willing to let this run overnight, even 
though this *should* work).

I want to come back to this and think about reverse engineering the program. 
"""

class Computer:
    def __init__(self, register_A, register_B, register_C):
        self.pointer = 0
        self.values = {
            0: 0,
            1: 1,
            2: 2,
            3: 3,
            4: register_A,
            5: register_B,
            6: register_C,
            7: None # Reserved.
        }
        self.instructions = {
            0: self._adv,
            1: self._bxl,
            2: self._bst,
            3: self._jnz,
            4: self._bxc,
            5: self._out,
            6: self._bdv,
            7: self._cdv
        }

    def _adv(self, operand):
        # Write the division to the A register.
        self.values[4] = self.values[4] // 2**self.values[operand]
        self._update_pointer()

    def _bxl(self, operand):
        # Write the XOR to the B register.
        self.values[5] = self.values[5] ^ operand
        self._update_pointer()

    def _bst(self, operand):
        # Write the modulo 8 to the B register.
        self.values[5] = self.values[operand] % 8
        self._update_pointer()

    def _jnz(self, operand):
        # If register A is 0, do nothing; else, jump the pointer.
        if self.values[4] != 0:
            self.pointer = operand
        else:
            self._update_pointer()

    def _bxc(self, operand):
        # Write the XOR to the B register.
        self.values[5] = self.values[5] ^ self.values[6]
        self._update_pointer()

    def _out(self, operand):
        self._update_pointer()
        return self.values[operand] % 8

    def _bdv(self, operand):
        # Write the division to the B register.
        self.values[5] = self.values[4] // 2**self.values[operand]
        self._update_pointer()

    def _cdv(self, operand):
        # Write the division to the C register.
        self.values[6] = self.values[4] // 2**self.values[operand]
        self._update_pointer()

    def _update_pointer(self):
        self.pointer += 2


with open("../_tests/day17.txt") as f:
    lines = f.readlines()

# PART 1.
# Initialize register values.
register_A = int(lines[0].split()[-1])
register_B = int(lines[1].split()[-1])
register_C = int(lines[2].split()[-1])

# Read program instructions.
program = lines[-1].split()[-1]
program = [int(x) for x in program.split(',')]

# Process instructions until the pointer is past the last instruction.
computer = Computer(register_A, register_B, register_C)
output = []
while 0 <= computer.pointer < len(program):
    opcode = program[computer.pointer]
    operand = program[computer.pointer+1]
    out_val = computer.instructions[opcode](operand)
    # Store results from the `out` instruction.
    if out_val is not None:
        output.append(out_val)

s = ','.join(map(str, output))
print(f'PART 1\tProgram output: {s}')
