from pathlib import Path

inputfile = Path(__file__).parent / "input.txt"
with open(inputfile) as f:
    lines = f.readlines()

sum = 0

for line in lines:
    # TODO
    sum = sum + 1

print('Part 1a: ' + str(sum))