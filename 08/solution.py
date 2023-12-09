from pathlib import Path

inputfile = Path(__file__).parent / "input.txt"
with open(inputfile) as f:
    lines = f.readlines()

# steps = "LLR"
steps = "LRLRRRLRLLRRLRLRRRLRLRRLRRLLRLRRLRRLRRRLRRRLRLRRRLRLRRLRRLLRLRLLLLLRLRLRRLLRRRLLLRLLLRRLLLLLRLLLRLRRLRRLRRRLRRRLRRLRRLRRRLRLRLRRLRLRLRLRRLRRRLLRLLRRLRLRRRLRLRRRLRLRRRLRRRLRRLRLLLLRLRRRLRLRRLRLRRLRRLRRLLRRRLLLLLLRLRRRLRRLLRRRLRRLLLRLRLRLRRRLRRLRLRRRLRRLRRRLLRRLRRLLLRRRR"

nodes = dict()
for line in lines:
    segments = line.split('=')
    key = segments[0].strip()
    pair = segments[1].replace('(', '').replace(')', '').split(',')
    left = pair[0].strip()
    right = pair[1].strip()

    nodes[key] = (left, right)

currentNode = "AAA"
currentStep = 0
while currentNode != "ZZZ":
    direction = steps[currentStep % len(steps)]
    if (direction == 'L'):
        currentNode = nodes[currentNode][0]
    else:
        currentNode = nodes[currentNode][1]

    currentStep = currentStep + 1
    # print (currentNode)
    if (currentStep % len(steps) == 0):
        print("Returning to top of input")

print('Steps: ' + str(currentStep))