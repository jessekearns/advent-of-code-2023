from pathlib import Path

inputfile = Path(__file__).parent / "input.txt"
with open(inputfile) as f:
    lines = f.readlines()

sum = 0

for line in lines:
    first = -1
    last = -1
    for element in line:
        if element.isdigit():
            if first < 0:
                first = int(element)
            last = int(element)
    sum += first * 10
    sum += last

print('Part 1: ' + str(sum))

newSum = 0

for line in lines:
    first = -1
    last = -1

    for i in range(0, len(line)):
        numeral = -1
        if line[i].isdigit():
            numeral = int(line[i])
        elif line[i:len(line)].startswith('one'):
            numeral = 1
        elif line[i:len(line)].startswith('two'):
            numeral = 2
        elif line[i:len(line)].startswith('three'):
            numeral = 3
        elif line[i:len(line)].startswith('four'):
            numeral = 4
        elif line[i:len(line)].startswith('five'):
            numeral = 5
        elif line[i:len(line)].startswith('six'):
            numeral = 6
        elif line[i:len(line)].startswith('seven'):
            numeral = 7
        elif line[i:len(line)].startswith('eight'):
            numeral = 8
        elif line[i:len(line)].startswith('nine'):
            numeral = 9

        if numeral > -1:
            if first < 0:
                first = numeral
            last = numeral

    newSum += first * 10
    newSum += last

print('Part 2: ' + str(newSum))