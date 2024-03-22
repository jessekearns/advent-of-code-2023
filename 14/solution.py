from pathlib import Path

def TiltNorth(grid):
    for i in range(0, len(grid[0])):
        availableTile = -1
        for j in range(0, len(grid)):
            if grid[j][i] == 'O' and availableTile >= 0:
                grid[availableTile] = grid[availableTile][:i] + 'O' + grid[availableTile][i + 1:]
                grid[j] = grid[j][:i] + '.' + grid[j][i + 1:]
                while availableTile < j and grid[availableTile][i] != '.':
                    availableTile = availableTile + 1
            elif grid[j][i] == '#':
                availableTile = -1
            elif grid[j][i] == '.' and availableTile < 0:
                availableTile = j

def TiltSouth(grid):
    for i in reversed(range(0, len(grid[0]))):
        availableTile = -1
        for j in reversed(range(0, len(grid))):
            if grid[j][i] == 'O' and availableTile >= 0:
                grid[availableTile] = grid[availableTile][:i] + 'O' + grid[availableTile][i + 1:]
                grid[j] = grid[j][:i] + '.' + grid[j][i + 1:]
                while availableTile > j and grid[availableTile][i] != '.':
                    availableTile = availableTile - 1
            elif grid[j][i] == '#':
                availableTile = -1
            elif grid[j][i] == '.' and availableTile < 0:
                availableTile = j

def TiltWest(grid):
    for j in range(0, len(grid)):
        availableTile = -1
        for i in range(0, len(grid[0])):
            if grid[j][i] == 'O' and availableTile >= 0:
                grid[j] = grid[j][:availableTile] + 'O' + grid[j][availableTile+1:i] + '.' +  grid[j][i+1:]
                while availableTile < i and grid[j][availableTile] != '.':
                    availableTile = availableTile + 1
            elif grid[j][i] == '#':
                availableTile = -1
            elif grid[j][i] == '.' and availableTile < 0:
                availableTile = i
                
def TiltEast(grid):
    for j in reversed(range(0, len(grid))):
        availableTile = -1
        for i in reversed(range(0, len(grid[0]))):
            if grid[j][i] == 'O' and availableTile >= 0:
                grid[j] = grid[j][:i] + '.' + grid[j][i+1:availableTile] + 'O' +  grid[j][availableTile+1:]
                while availableTile > i and grid[j][availableTile] != '.':
                    availableTile = availableTile - 1
            elif grid[j][i] == '#':
                availableTile = -1
            elif grid[j][i] == '.' and availableTile < 0:
                availableTile = i

def SpinCycle(grid):
    TiltNorth(grid)
    TiltWest(grid)
    TiltSouth(grid)
    TiltEast(grid)

def PrintGrid(grid):
    for j in range(0, len(grid)):
        print(grid[j])

def CalculateLoad(grid):
    load = 0
    for i in range(0, len(grid[0])):
        for j in range(0, len(grid)):
            if grid[j][i] == 'O':
                load = load + len(grid) - j
    return load

inputfile = Path(__file__).parent / "input.txt"
with open(inputfile) as f:
    lines = f.readlines()

initialCycles = 100
guessedMaxRepetitionLength = 50
guessedMinRepetitionLength = 5
maxCycles = 1000000000

grid = []
for line in lines:
    grid.append(line.replace('\n', ''))

TiltNorth(grid)
print('Load after tilting north: ' + str(CalculateLoad(grid)))

# Advance to a point where repetition is likely
for cycleCount in range(0, initialCycles):
    SpinCycle(grid)
    # print('Cycle ' + str(cycleCount + 1) + ': ' + str(CalculateLoad(grid)))

# Keep advancing, and record the values after each cycle for lookback when determining a repetition
values = []
initialPosition = -1
initialValue = -1
for cycleCount in range(0, guessedMaxRepetitionLength * 2):
    SpinCycle(grid)
    load = CalculateLoad(grid)
    values.append(load)

repetitionSize = 0
# Loop through the list and check for a repeating pattern
for cycleCount in range(guessedMinRepetitionLength, guessedMaxRepetitionLength):
    if values[0] != values[cycleCount]:
        continue
    repetitionFound = True
    for i in range(1, cycleCount):
        if values[i] != values[cycleCount + i]:
            repetitionFound = False
            break
    if repetitionFound:
        repetitionSize = cycleCount
        break

if repetitionSize == 0:
    print('No dice! Pick a bigger repetition length estimate.')
else:
    print('Cycle size: ' + str(repetitionSize))
    # for i in range(0, repetitionSize):
    #     cycle = initialCycles + i + 1
    #     print('Cycle ' + str(cycle) + ': ' + str(values[i]))

    skippedRepetitions = int((maxCycles - initialCycles) / repetitionSize)
    for i in range(0, repetitionSize):
        cycle = initialCycles + i + 1 + (skippedRepetitions * repetitionSize)
        print('Cycle ' + str(cycle) + ': ' + str(values[i]))