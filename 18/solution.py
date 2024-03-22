from pathlib import Path

inputfile = Path(__file__).parent / "input.txt"
with open(inputfile) as f:
    lines = f.readlines()

# Start by getting dimensions
minX = 0
minY = 0
maxX = 0
maxY = 0
currX = 0
currY = 0
for line in lines:
    direction = line.split(' ')[0]
    steps = int(line.split(' ')[1])
    if direction == 'R':
        currX = currX + steps
    if direction == 'L':
        currX = currX - steps
    if direction == 'D':
        currY = currY + steps
    if direction == 'U':
        currY = currY - steps
    if currY < minY:
        minY = currY
    if currY > maxY:
        maxY = currY
    if currX < minX:
        minX = currX
    if currX > maxX:
        maxX = currX

# Adjust start positions so the grid is zero-indexed
currX = 0
if minX < 0:
    maxX = maxX + abs(minX)
    currX = currX + abs(minX)
currY = 0
if minY < 0:
    maxY = maxY + abs(minY)
    currY = currY + abs(minY)

# Initialize grid
grid = []
for y in range(0, maxY + 1):
    row = []
    for x in range(0, maxX + 1):
        row.append('.')
    grid.append(row)

# Update grid by following instructions
for line in lines:
    direction = line.split(' ')[0]
    steps = int(line.split(' ')[1])
    for step in range(0, steps):
        if direction == 'R':
            currX = currX + 1
        if direction == 'L':
            currX = currX - 1
        if direction == 'D':
            currY = currY + 1
        if direction == 'U':
            currY = currY - 1
        grid[currY][currX] = '#'

# Sum dug-out portions
sum = 0
for row in grid:
    startIndex = 0
    endIndex = maxX
    while row[startIndex] != '#':
        startIndex = startIndex + 1
    while row[endIndex] != '#':
        endIndex = endIndex - 1
    sum = sum + (endIndex - startIndex) + 1

# Print grid
output = ''
for row in grid:
    output = output + '|'
    for c in row:
        output = output + c
    output = output + '|\n'
print(output)


print('Part 1: ' + str(sum))