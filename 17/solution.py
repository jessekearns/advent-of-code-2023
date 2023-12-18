from pathlib import Path
import copy
import time

class PathInfo:
    def __init__(self, currentCost, currentConsecutiveMoves, direction, steps):
        self.currentCost = currentCost
        self.currentConsecutiveMoves = currentConsecutiveMoves
        self.direction = direction
        self.steps = steps

    def IsBetterThan(self, other):
        return self.direction == other.direction and self.currentCost <= other.currentCost and self.currentConsecutiveMoves <= other.currentConsecutiveMoves

class CombinedPathInfo:
    def __init__(self):
        self.paths = []

    def AddPathInfo(self, newPath):
        # If any existing path is strictly better than this one, skip adding it
        for existingPath in self.paths:
            if existingPath.IsBetterThan(newPath):
                return False
        
        # If an existing path is strictly worse than this one, remove the existing path before adding
        i = 0
        while i < len(self.paths):
            if newPath.IsBetterThan(self.paths[i]):
                del(self.paths[i])
                i = i - 1
            i = i + 1

        # At this point, any remaining paths are better than the new one in at least one dimension. Add the new one sorted by cost descending
        i = 0
        while i < len(self.paths) and self.paths[i].currentCost > newPath.currentCost:
            i = i + 1
        self.paths.insert(i, newPath)
        return True

    def GetShortestPath(self, minConsecutiveMoves):
        if len(self.paths) == 0:
            return float('inf')
        for i in reversed(range(0, len(self.paths))):
            if self.paths[i].currentConsecutiveMoves >= minConsecutiveMoves:
                return self.paths[i].currentCost
        return float('inf')
    
    def GetShortestPartialPath(self):
        if len(self.paths) == 0:
            return float('inf')
        return self.paths[-1].currentCost
    
    def GetShortestPathInfo(self, minConsecutiveMoves):
        for i in reversed(range(0, len(self.paths))):
            if self.paths[i].currentConsecutiveMoves >= minConsecutiveMoves:
                return self.paths[i]
    
    def GetShortestPartialPathInfo(self):
        return self.paths[-1]     
    
    def PrintShortestPath(self, minConsecutiveMoves):
        pathInfo = self.GetShortestPathInfo(minConsecutiveMoves)
        for y in range(0, yMax):
            output = ''
            for x in range(0, xMax):
                if (x, y) in pathInfo.steps:
                    output = output + '*'
                else:
                    output = output + str(grid[y][x])
            print(output)
        print('')

    def PrintPathOptions(self):
        for path in self.paths:
            output = 'Cost ' + str(path.currentCost) + ', Consective Moves ' + str(path.currentConsecutiveMoves) + ', Direction ' + str(path.direction)
            print(output)
        print('')


def GetKey(x, y, xMax):
    return (y * xMax) + x

# Part 1 = 3 and 1, Part 2 = 10 and 4
maxConsecutiveMoves = 10
minConsecutiveMoves = 4

inputfile = Path(__file__).parent / "input.txt"
with open(inputfile) as f:
    lines = f.readlines()

grid = []
for line in lines:
    row = []
    for c in line:
        if c != '\n':
            row.append(int(c))
    grid.append(row)

xMax = len(grid[0])
yMax = len(grid)
nodeCosts = dict()
for x in range (0, xMax):
    for y in range(0, yMax):
        key = GetKey(x, y, xMax)
        nodeCosts[key] = CombinedPathInfo()

nodeCosts[GetKey(0, 0, xMax)].AddPathInfo(PathInfo(0, 0, 0, [(0, 0)]))
nextCandidates = []
nextCandidates.append((0,0))

startTime = time.time()
while len(nextCandidates) > 0:
    # Find the nextCandidate with the lowest cost
    bestCost = float('inf')
    bestCandidate = (-1, -1)

    i = 0
    while i < len(nextCandidates):
        candidate = nextCandidates[i]
        key = GetKey(candidate[0], candidate[1], xMax)

        cost = nodeCosts[key].GetShortestPath(minConsecutiveMoves)
        if cost < bestCost:
            bestCost = cost
            bestCandidate = candidate
        i = i + 1

    if bestCandidate[0] == -1:
        i = 0
        while i < len(nextCandidates):
            candidate = nextCandidates[i]
            key = GetKey(candidate[0], candidate[1], xMax)

            cost = nodeCosts[key].GetShortestPartialPath()
            if cost < bestCost:
                bestCost = cost
                bestCandidate = candidate
            i = i + 1

    curr = bestCandidate
    nextCandidates.remove(curr)
    key = GetKey(curr[0], curr[1], xMax)

    # print('Visiting ' + str(curr[0]) + ', ' + str(curr[1]))

    currentPaths = nodeCosts[key]

    directions = [0, 1, 2, 3]
    for direction in directions:
        additionalCost = 0
        additionalSteps = []
        for i in range (1, maxConsecutiveMoves + 1):
            if direction == 0:
                neighbor = (curr[0] + i, curr[1])
            elif direction == 1:
                neighbor = (curr[0], curr[1] + i)
            elif direction == 2:
                neighbor = (curr[0] - i, curr[1])
            else:
                neighbor = (curr[0], curr[1] - i)

            if neighbor[0] < 0 or neighbor[0] >= xMax or neighbor[1] < 0 or neighbor[1] >= yMax:
                continue

            additionalCost = additionalCost + grid[neighbor[1]][neighbor[0]]
            additionalSteps.append(neighbor)
            neighborKey = GetKey(neighbor[0], neighbor[1], xMax)
            neighborImproved = False

            for path in nodeCosts[key].paths:
                # Skip a full 180 turn
                if (path.direction + 2) % 4 == direction:
                    continue

                newConsecutiveMoves = i
                if path.direction == direction:
                    newConsecutiveMoves = path.currentConsecutiveMoves + newConsecutiveMoves

                # Skip moves that aren't within range
                if newConsecutiveMoves < minConsecutiveMoves or newConsecutiveMoves > maxConsecutiveMoves:
                    continue

                newCost = path.currentCost + additionalCost
                newSteps = copy.deepcopy(path.steps)
                for step in additionalSteps:
                    newSteps.append(step)
                newPathInfo = PathInfo(newCost, newConsecutiveMoves, direction, newSteps)
                neighborImproved = nodeCosts[neighborKey].AddPathInfo(newPathInfo) or neighborImproved

            if neighborImproved and neighbor not in nextCandidates:
                nextCandidates.append(neighbor)

endTime = time.time()
print(f"Iteration finished after {endTime-startTime} seconds")

# testKey1 = GetKey(xMax - 5, 0, xMax)
# print('Test 1:')
# nodeCosts[testKey1].PrintPathOptions()
# nodeCosts[testKey1].PrintShortestPath(minConsecutiveMoves)

# testKey1 = GetKey(xMax - 1, yMax - 2, xMax)
# print('Test 2:')
# nodeCosts[testKey1].PrintShortestPath()

targetKey = GetKey(xMax - 1, yMax - 1, xMax)
print('Lowest-cost path to goal: ' + str(nodeCosts[targetKey].GetShortestPath(minConsecutiveMoves)))
# nodeCosts[targetKey].PrintPathOptions()
nodeCosts[targetKey].PrintShortestPath(minConsecutiveMoves)