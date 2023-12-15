from pathlib import Path

def compareRows(str1, str2, smudgesRemaining):
    if smudgesRemaining == 0:
        return (str1 == str2, 0)
    
    smudgesUsed = 0
    for i in range(0, len(str1)):
        if str1[i] == str2[i]:
            continue
        elif smudgesUsed < smudgesRemaining:
            smudgesUsed = smudgesUsed + 1
        else:
            return (False, 0)
        
    return (True, smudgesUsed)

inputfile = Path(__file__).parent / "input.txt"
with open(inputfile) as f:
    lines = f.readlines()

allowedSmudges = 1 # 0 for Part 1, 1 for Part 2
grids = []
newGrid = []

for line in lines:
    if len(line) == 1:
        grids.append(newGrid)
        newGrid = []
    else:
        newGrid.append(line.replace('\n', ''))
grids.append(newGrid)

reflectionSum = 0
for grid in grids:
    reflectionValue = -1
    maxHeight =  len(grid)
    maxWidth = len(grid[0])

    for i in range(1, maxHeight):
        compareResult = compareRows(grid[i-1], grid[i], allowedSmudges)
        if compareResult[0]:
            j = i+1
            k = i-2
            remainingSmudges = allowedSmudges - compareResult[1]
            while j < maxHeight and k >= 0:
                compareResult = compareRows(grid[j], grid[k], remainingSmudges)
                if compareResult[0] == False:
                    break
                remainingSmudges = remainingSmudges - compareResult[1]
                j = j + 1
                k = k - 1
            if remainingSmudges == 0 and (j >= maxHeight or k < 0):
                reflectionValue = i * 100
                print('Horizontal reflection line found: ' + str(i))
                break

    if reflectionValue > 0:
        reflectionSum = reflectionSum + reflectionValue
        continue

    pivotedGrid = []
    for x in range (0, maxWidth):
        newRow = ''
        for y in range (0, maxHeight):
            newRow = newRow + grid[y][x]
        pivotedGrid.append(newRow)

    for i in range(1, maxWidth):
        compareResult = compareRows(pivotedGrid[i-1], pivotedGrid[i], allowedSmudges)
        if compareResult[0]:
            j = i+1
            k = i-2
            remainingSmudges = allowedSmudges - compareResult[1]
            while j < maxWidth and k >= 0:
                compareResult = compareRows(pivotedGrid[j], pivotedGrid[k], remainingSmudges)
                if compareResult[0] == False:
                    break
                remainingSmudges = remainingSmudges - compareResult[1]
                j = j + 1
                k = k - 1
            if remainingSmudges == 0 and (j >= maxWidth or k < 0):
                reflectionValue = i
                print('Vertical reflection line found: ' + str(i))
                break

    if reflectionValue > 0:
        reflectionSum = reflectionSum + reflectionValue
    else:
        print('No reflection found')

print('Summary: ' + str(reflectionSum))