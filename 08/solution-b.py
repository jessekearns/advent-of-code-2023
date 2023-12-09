from pathlib import Path

inputfile = Path(__file__).parent / "input.txt"
with open(inputfile) as f:
    lines = f.readlines()

# steps = "LR"
steps = "LRLRRRLRLLRRLRLRRRLRLRRLRRLLRLRRLRRLRRRLRRRLRLRRRLRLRRLRRLLRLRLLLLLRLRLRRLLRRRLLLRLLLRRLLLLLRLLLRLRRLRRLRRRLRRRLRRLRRLRRRLRLRLRRLRLRLRLRRLRRRLLRLLRRLRLRRRLRLRRRLRLRRRLRRRLRRLRLLLLRLRRRLRLRRLRLRRLRRLRRLLRRRLLLLLLRLRRRLRRLLRRRLRRLLLRLRLRLRRRLRRLRLRRRLRRLRRRLLRRLRRLLLRRRR"

currentNodes = []
successfulIntervals = []

nodes = dict()
for line in lines:
    segments = line.split('=')
    key = segments[0].strip()
    pair = segments[1].replace('(', '').replace(')', '').split(',')
    left = pair[0].strip()
    right = pair[1].strip()

    if (key[2] == 'A'):
        currentNodes.append(key)
    nodes[key] = (left, right)


currentStep = 0
while len(currentNodes) > 0:
    direction = steps[currentStep % len(steps)]
    directionIndex = 0
    if (direction == 'R'):
        directionIndex = 1

    newNodes = []
    for current in currentNodes:
        newNode = nodes[current][directionIndex]
        if newNode[2] == 'Z':
            successfulIntervals.append(currentStep + 1)
        else:
            newNodes.append(newNode)

    currentNodes = newNodes
    currentStep = currentStep + 1

print('LCM of: ' + str(successfulIntervals))