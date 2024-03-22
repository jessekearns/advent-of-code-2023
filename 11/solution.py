from pathlib import Path

inputfile = Path(__file__).parent / "input.txt"
with open(inputfile) as f:
    grid = f.readlines()

expansionFactor = 999999 # 1 for part 1, (1M-1) for part 2

y = 0
verticalExpansionIndices = []
# Expand vertically
for row in grid:
    galaxyFound = False
    for c in row:
        if c =='#':
            galaxyFound = True
    if not galaxyFound:
        verticalExpansionIndices.append(y)
    y = y + 1

# Expand horizontally
horizontalExpansionIndices = []
for x in range(0, len(grid[0]) - 1):
    galaxyFound = False
    for y in range(0, len(grid)):
        if grid[y][x] == '#':
            galaxyFound = True
    if not galaxyFound:
        horizontalExpansionIndices.append(x)

xMax = len(grid[0]) - 1
yMax = len(grid)
galaxies = []
for x in range(0, xMax):
    for y in range(0, yMax):
        if grid[y][x] == '#':
            galaxies.append((x, y))
            # print((x, y))

adjustedGalaxies = []
for galaxy in galaxies:
    newX = galaxy[0]
    for horizontalExp in horizontalExpansionIndices:
        if galaxy[0] > horizontalExp:
            newX = newX + expansionFactor

    newY = galaxy[1]
    for verticalExp in verticalExpansionIndices:
        if galaxy[1] > verticalExp:
            newY = newY + expansionFactor

    adjustedGalaxies.append((newX, newY))

distances = dict()
for a in range (0, len(adjustedGalaxies) - 1):
    for b in range(a + 1, len(adjustedGalaxies)):
        gA = adjustedGalaxies[a]
        gB = adjustedGalaxies[b]
        distance = abs(gA[0] - gB[0]) + abs(gA[1] - gB[1])
        distances[(gA, gB)] = distance

sum = 0
for key in distances:
    # print(str(key) + ': ' + str(distances[key]))
    sum = sum + distances[key]

print('Sum of lengths: ' + str(sum))