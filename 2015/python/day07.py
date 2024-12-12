"""
Advent of Code 2015
Day 7: Some Assembly Required

This was a fun one!

I'm quite satisfied with my final implementation. I must give credit to
a couple Reddit tips to use exception handling and a double-ended queue. I 
initially declared the wires as local variables, which worked, but I opted for 
a hash map implementation in this final version for cleaner code.

The idea is to create a list of circuit instructions and execute it until all
instructions evaluate successfully; this happens once all wires have a signal
and the circuit is complete. The `exec` function, which I hadn't heard of
before, was perfect for this.
"""

from collections import deque


with open("../_tests/day07.txt") as f:
    instructions = f.read().splitlines()

# Wire signals will be stored in a hash map.
circuit = {}
# Use Python's bit operators to emulate the gates.
ops = {
    "AND": '&',
    "OR": '|',
    "NOT": '~',
    "RSHIFT": '>>',
    "LSHIFT": '<<'
}

circuit_instructions = deque()
for instruction in instructions:
    parsed_instruction = instruction.split(" -> ")
    gate = parsed_instruction[0]
    wire = parsed_instruction[1]

    # Parse the gate into a Python expression involving a bit operator.
    for op, symbol in ops.items():
        if op in gate:
            gate = gate.replace(op, symbol)
            # There's only one binary operator per instruction.
            break
    
    # Lookup signal(s) so that the expression can be executed with `exec`.
    tokens = []
    for token in gate.split():
        if token.isalpha():
            token = f'circuit["{token}"]'
        tokens.append(token)
    gate = ' '.join(tokens)

    circuit_instruction = f'circuit["{wire}"] = {gate}'
    circuit_instructions.append(circuit_instruction)

# Execute the instructions until the circuit is complete, i.e., once all wires
# have a signal.
completed_instructions = []
while circuit_instructions:
    instruction = circuit_instructions.popleft()
    try:
        exec(instruction)
        completed_instructions.append(instruction)
    except KeyError:
        circuit_instructions.append(instruction)

# PART 1.
# Note: Neither wire `a`` nor `b` are present in the test input, so this 
# will throw an error.
print(f'PART 1\tSignal in wire a: {circuit["a"]}')

# PART 2.
circuit["b"] = circuit["a"]
for instruction in completed_instructions:
    # Reset all signals except the assignment to "b".
    if not instruction.startswith('circuit["b"] ='):
        exec(instruction)

print(f'PART 2\tNew signal in wire a: {circuit["a"]}')
