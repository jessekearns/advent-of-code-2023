from pathlib import Path

class Beam:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.hasSplit = False

    def Terminated(self, grid):
        xMax = len(grid[0])
        yMax = len(grid)
        return self.x < 0 or self.y < 0 or self.x >= xMax or self.y >= yMax

    def Advance(self, grid):
        self.hasSplit = False
        xMax = len(grid[0])
        yMax = len(grid)
        if self.Terminated(grid):
            print('Why am I being run?')
            return
        
        if self.direction == 0: # Right
            if grid[self.y][self.x] == '.' or grid[self.y][self.x] == '-':
                self.x = self.x + 1
            elif grid[self.y][self.x] == '|':
                self.direction = 1
                self.hasSplit = True
                self.y = self.y + 1
            elif grid[self.y][self.x] == '/':
                self.direction = 3
                self.y = self.y - 1
            elif grid[self.y][self.x] == '\\':
                self.direction = 1
                self.y = self.y + 1

        elif self.direction == 1: # Down
            if grid[self.y][self.x] == '.' or grid[self.y][self.x] == '|':
                self.y = self.y + 1
            elif grid[self.y][self.x] == '/':
                self.direction = 2
                self.x = self.x - 1
            elif grid[self.y][self.x] == '-':
                self.direction = 0
                self.hasSplit = True
                self.x = self.x + 1
            elif grid[self.y][self.x] == '\\':
                self.direction = 0
                self.x = self.x + 1

        elif self.direction == 2: # Left
            if grid[self.y][self.x] == '.' or grid[self.y][self.x] == '-':
                self.x = self.x - 1
            elif grid[self.y][self.x] == '|':
                self.direction = 1
                self.hasSplit = True
                self.y = self.y + 1
            elif grid[self.y][self.x] == '/':
                self.direction = 1
                self.y = self.y + 1
            elif grid[self.y][self.x] == '\\':
                self.direction = 3
                self.y = self.y - 1

        elif self.direction == 3: # Up
            if grid[self.y][self.x] == '.' or grid[self.y][self.x] == '|':
                self.y = self.y - 1
            elif grid[self.y][self.x] == '/':
                self.direction = 0
                self.x = self.x + 1
            elif grid[self.y][self.x] == '-':
                self.direction = 0
                self.hasSplit = True
                self.x = self.x + 1
            elif grid[self.y][self.x] == '\\':
                self.direction = 2
                self.x = self.x - 1

    def GetSplitBeam(self):
        newDirection = (self.direction + 2) % 4
        newX = self.x
        newY = self.y
        if self.direction == 0:
            newX = newX - 2
        elif self.direction == 1:
            newY = newY - 2
        elif self.direction == 2:
            newX = newX + 2
        elif self.direction == 3:
            newY = newY + 2 

        return Beam(newX, newY, newDirection)


inputfile = Path(__file__).parent / "input.txt"
with open(inputfile) as f:
    lines = f.readlines()

grid = []
for line in lines:
    grid.append(line.replace('\n', ''))

xMax = len(grid[0])
yMax = len(grid)
# initialBeams = [Beam(0, 0, 0)] # Part 1
# Part 2
initialBeams = []
for x in range(0, xMax):
    initialBeams.append(Beam(x, 0, 1))
    initialBeams.append(Beam(x, yMax - 1, 3))
for y in range(0, yMax):
    initialBeams.append(Beam(0, y, 0))
    initialBeams.append(Beam(xMax - 1, y, 2))

maxEnergy = 0
for initialBeam in initialBeams:
    allBeams = [initialBeam]
    energizedTiles = dict()

    while len(allBeams) > 0:
        # Skip processing terminated beams
        if allBeams[0].Terminated(grid):
            allBeams.pop(0)
            continue

        # If we've already processed a beam through this tile in this direction, terminate to avoid an infinite loop
        # Else, Update our record of energized tiles and beams passing through them in each direction
        key = str(allBeams[0].x) + ',' + str(allBeams[0].y)
        if key not in energizedTiles:
            energizedTiles[key] = [False, False, False, False]
        
        if energizedTiles[key][allBeams[0].direction] == True:
            allBeams.pop(0)
            continue

        energizedTiles[key][allBeams[0].direction] = True

        # Check if we've split and append the new beam to the list
        if allBeams[0].hasSplit:
            allBeams.append(allBeams[0].GetSplitBeam())

        # Finally, advance the beam
        allBeams[0].Advance(grid)

    if len(energizedTiles) > maxEnergy:
        maxEnergy = len(energizedTiles)

    # for y in range(0, len(grid)):
    #     adjustedRow = ''
    #     for x in range(0, len(grid[0])):
    #         key = str(x) + ',' + str(y)
    #         if key in energizedTiles:
    #             adjustedRow = adjustedRow + '#'
    #         else:
    #             adjustedRow = adjustedRow + grid[y][x]
    #     print(adjustedRow)

print('Energized Tiles: ' + str(maxEnergy))