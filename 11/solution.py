from pathlib import Path

inputfile = Path(__file__).parent / "input.txt"
with open(inputfile) as f:
    lines = f.readlines()

grid = []

# Expand vertically
for line in lines:
    galaxyFound = False
    for c in line:
        if c =='#':
            galaxyFound = True

    grid.append(line)
    if(not galaxyFound):
        grid.append(line)

# Expand horizontally
horizontalExpansionIndices = []
for x in range(0, len(grid[0]) - 1):
    galaxyFound = False
    for y in range(0, len(grid)):
        if grid[y][x] == '#':
            galaxyFound = True
    if(not galaxyFound):
        horizontalExpansionIndices.append(x)

newGrid = []

horizontalExpansionIndices.reverse() # Start from the right edge to avoid index math as we expand
for row in grid:
    for i in horizontalExpansionIndices:
        row = row[:i] + '.' + row[i:]
    newGrid.append(row)

grid = newGrid

xMax = len(grid[0]) - 1
yMax = len(grid)
galaxies = []
for x in range(0, xMax):
    for y in range(0, yMax):
        if grid[y][x] == '#':
            galaxies.append((x, y))

distances = dict()
for a in range (0, len(galaxies) - 1):
    for b in range(a + 1, len(galaxies)):
        gA = galaxies[a]
        gB = galaxies[b]
        # Sort for redundancy checking: A should be less than B
        if gA[0] > gB[0] or (gA[0] == gB[0] and gA[1] > gB[1]):
            temp = gA
            gA = gB
            gB = temp
        distances[(gA, gB)] = abs(gA[0] - gB[0]) + abs(gA[1] - gB[1])

sum = 0
for key in distances:
    sum = sum + distances[key]

print('Sum of lengths: ' + str(sum))