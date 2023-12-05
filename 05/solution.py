from pathlib import Path
import copy

inputfile = Path(__file__).parent / "input.txt"
with open(inputfile) as f:
    lines = f.readlines()

previousValues = []
currentValues = []
currentMapping = "seeds"
seedsAreRanges = True # Toggle for part 1 vs part 2

for line in lines:
    # Skip empty line
    if len(line) <= 1:
        continue

    # Check non-numeral line
    if ':' in line:
        # This is the initial set of seeds
        if 'seeds:' in line:
            seedStrings = line.split(':')[1].strip().split(' ')

            seedsTemp = 0
            for seedString in seedStrings:
                if seedStrings != '\n' and seedString != '':
                    if not seedsAreRanges:
                        currentValues.append(int(seedString))
                    elif seedsTemp == 0:
                        seedsTemp = int(seedString)
                    else:
                        for i in range(0, int(seedString)):
                            currentValues.append(seedsTemp + i)
                        seedsTemp = 0


        # This is a new mapping
        else:
            # Copy over any unmapped values.
            for prev in previousValues:
                currentValues.append(prev)

            print('Values after ' + currentMapping + ': ' + str(currentValues))

            previousValues = currentValues
            currentValues = []
            currentMapping = line.split(' ')[0]
    
    # Parse the numeral line
    else:
        nums = line.split(' ')
        destination = int(nums[0])
        source = int(nums[1])
        rangeLength = int(nums[2])

        prevCopy = copy.deepcopy(previousValues)
        for prev in prevCopy:
            if prev >= source and prev < source + rangeLength:
                diff = prev - source
                currentValues.append(destination + diff)
                previousValues.remove(prev)

for prev in previousValues:
    currentValues.append(prev)

print('Values after ' + currentMapping + ': ' + str(currentValues))

lowest = currentValues[0]
for val in currentValues:
    if (val < lowest):
        lowest = val

print('Lowest Location: ' + str(lowest))