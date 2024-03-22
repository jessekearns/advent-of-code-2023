from pathlib import Path
import copy

def CheckExteriorSpace(x, y, maze, allLoopedLengths, nonLoopedSpaces):
    xMax = len(maze[0]) - 1 # Handle line terminator
    yMax = len(maze)

    queue = [(x, y)]
    processed = []
    outsideReached = False

    while len(queue) > 0:
        curr = queue.pop(0)
        # Check out of bounds
        if curr[0] < 0 or curr[0] >= xMax or curr[1] < 0 or curr[1] >= yMax:
            continue

        # Check for the edge of the main loop or already iterated items
        if curr in allLoopedLengths or curr in processed:
            continue

        # Check for the edge of the grid
        if curr[0] == 0 or curr[1] == 0 or curr[0] == xMax - 1 or curr[1] == yMax - 1:
            outsideReached = True
        
        queue.append((curr[0]-1, curr[1]))
        queue.append((curr[0]+1, curr[1]))
        queue.append((curr[0], curr[1]-1))
        queue.append((curr[0], curr[1]+1))
        processed.append(curr)

    for coords in processed:
        nonLoopedSpaces[coords] = outsideReached

class PipeChecker:
    def __init__(self, x, y): 
        self.x = x
        self.y = y
        self.dictionary = dict()
        self.looped = False
        self.terminated = False
        self.steps = 0

    def advance(self, maze):
        # Check for terminal conditions first: Loop found, ground found, already terminated
        curr = maze[self.y][self.x]

        if self.terminated:
            return []
        if curr == 'S' and self.steps > 2:
            self.looped = True
            self.terminated = True
            return []       
        key = (self.x, self.y)
        if curr == '.' or key in self.dictionary:
            self.terminated = True
            return []

        # Record the current state and advance the step counter
        self.dictionary[key] = self.steps
        self.steps = self.steps + 1

        # Check next candidates for this pipe
        checkNorth = curr == 'S' or curr == '|' or curr == 'J' or curr == 'L'
        checkEast = curr == 'S' or curr == '-' or curr == 'F' or curr == 'L'
        checkSouth = curr == 'S' or curr == '|' or curr == '7' or curr == 'F'
        checkWest = curr == 'S' or curr == '-' or curr == '7' or curr == 'J'
        nextCoords = []
        xMax = len(maze[0]) - 1 # Handle line terminator
        yMax = len(maze)

        if (checkNorth):
            newY = self.y - 1
            newKey = (self.x, newY)
            if newY < 0:
                checkNorth = False
            else:
                next = maze[newY][self.x]
                if next == 'S' or next == '|' or next == '7' or next == 'F':
                    nextCoords.append(newKey)

        if (checkEast):
            newX = self.x + 1
            newKey = (newX, self.y)
            if newX > xMax:
                checkEast = False
            else:
                next = maze[self.y][newX]
                if next == 'S' or next == '-' or next == '7' or next == 'J':
                    nextCoords.append(newKey)

        if (checkSouth):
            newY = self.y + 1
            newKey = (self.x, newY)
            if newY >= yMax:
                checkSouth = False
            else:
                next = maze[newY][self.x]
                if next == 'S' or next == '|' or next == 'J' or next == 'L':
                    nextCoords.append(newKey)

        if (checkWest):
            newX = self.x - 1
            newKey = (newX, self.y)
            if newX < 0:
                checkWest = False
            else:
                next = maze[self.y][newX]
                if next == 'S' or next == '-' or next == 'F' or next == 'L':
                    nextCoords.append(newKey)

        # If there are no viable candidates, terminate
        if len(nextCoords) == 0:
            self.terminated = True
            return []
        
        newCheckers = []
        # If this is a branching point, spin up new checkers for all but the last candidate
        while len(nextCoords) > 1:
            next = nextCoords.pop(0)
            newChecker = PipeChecker(next[0], next[1])
            newChecker.steps = self.steps
            newChecker.dictionary = copy.deepcopy(self.dictionary)
            newCheckers.append(newChecker)
        
        # If there's exactly one viable candidate, advance to that space
        if len(nextCoords) == 1:
            self.x = nextCoords[0][0]
            self.y = nextCoords[0][1]
            return newCheckers


inputfile = Path(__file__).parent / "input.txt"
with open(inputfile) as f:
    maze = f.readlines()

xMax = len(maze[0]) - 1 # Handle line terminator
yMax = len(maze)
xStart = -1
yStart = -1

for x in range(0, xMax):
    for y in range(0, yMax):
        if maze[y][x] == 'S':
            xStart = x
            yStart = y
            break

unterminatedCheckers = []
unterminatedCheckers.append(PipeChecker(xStart, yStart))
allLoopedLengths = dict()

while len(unterminatedCheckers) > 0 and len(allLoopedLengths) == 0:
    # If the top checker has terminated, update our dictionary of lengths if a loop to the start was detected.
    if unterminatedCheckers[0].terminated:
        finishedChecker = unterminatedCheckers.pop(0)
        if finishedChecker.looped:
            for key in finishedChecker.dictionary:
                if key in allLoopedLengths:
                    allLoopedLengths[key] = max(allLoopedLengths[key], finishedChecker.dictionary[key])
                else:
                    allLoopedLengths[key] = finishedChecker.dictionary[key]
    else:
        newCheckers = unterminatedCheckers[0].advance(maze)
        for newChecker in newCheckers:
            unterminatedCheckers.append(newChecker)

# print(allLoopedLengths)

max = 0
for key in allLoopedLengths:
    if allLoopedLengths[key] > max:
        max = allLoopedLengths[key]

# Furthest out = total loop length /2
max = max + 1
max = int(max / 2)

print('Furthest out looped point: ' + str(max))

nonLoopedSpaces = dict()
for y in range(0, yMax):
    for x in range(0, xMax):
        CheckExteriorSpace(x, y, maze, allLoopedLengths, nonLoopedSpaces)

enclosedCounter = 0
for y in range(1, yMax - 1):
    crosses = 0
    for x in range(0, xMax):
        if (x, y) in allLoopedLengths:
            if maze[y][x] == '|' or maze[y][x] == 'F' or maze[y][x] == '7': # maze[y][x] == 'S' or  # or maze[y][x] == 'F' or maze[y][x] == '7': # or maze[y][x] == 'L' or maze[y][x] == 'J':
                diff = allLoopedLengths[(x, y)] - allLoopedLengths[(x, y+1)]
                crosses = crosses + diff
        elif (x, y) in nonLoopedSpaces and nonLoopedSpaces[(x, y)] == False:
            if crosses != 0:
                enclosedCounter = enclosedCounter + 1

print('Enclosed Spaces: ' + str(enclosedCounter))

# for y in range(0, yMax):
#     line = ""
#     for x in range(0, xMax):
#         if ((x, y)) in allLoopedLengths:
#             line = line + maze[y][x]
#         elif ((x, y)) in nonLoopedSpaces:
#             if nonLoopedSpaces[(x, y)]:
#                 line = line + 'O'
#             else:
#                 line = line + '*'
#         else:
#             line = line + maze[y][x]
#     print(line)