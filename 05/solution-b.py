from pathlib import Path
import copy

inputfile = Path(__file__).parent / "input.txt"
with open(inputfile) as f:
    lines = f.readlines()

previousValues = []
currentValues = []
currentMapping = "seeds"

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
                    if seedsTemp == 0:
                        seedsTemp = int(seedString)
                    else:
                        currentValues.append((seedsTemp, int(seedString)))
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
        mapStart = int(nums[1])
        mapEnd = int(nums[1]) + int(nums[2]) - 1

        prevCopy = copy.deepcopy(previousValues)
        prevPartials = []
        for prev in prevCopy:
            prevStart = prev[0]
            prevEnd = prev[0] + prev[1] - 1
            if prevStart <= mapEnd and mapStart <= prevEnd: # There exists an overlap
                previousValues.remove(prev)
                if prevStart >= mapStart and prevEnd <= mapEnd: # Complete overlap
                    newStart = (prevStart-mapStart) + destination
                    currentValues.append((newStart, prev[1]))
                else: # Partial overlap

                    # TODO Debug me
                    unmatched1 = [prevStart, 0]
                    matched = [max(prevStart, mapStart), 0]
                    unmatched2 = [min(prevEnd, mapEnd) + 1, 0]

                    unmatched1[1] = matched[0] - unmatched1[0]
                    matched[1] = unmatched2[0] - matched[0]                   
                    unmatched2[1] = prevEnd - unmatched2[0] + 1

                    # Solve this without looping
                    # for i in range(prevStart, prevEnd + 1):
                    #     if i < mapStart:
                    #         if unmatched1[0] == -1:
                    #             unmatched1[0] = i
                    #         unmatched1[1] = unmatched1[1] + 1
                    #     elif i > mapEnd:
                    #         if unmatched2[0] == -1:
                    #             unmatched2[0] = i
                    #         unmatched2[1] = unmatched2[1] + 1
                    #     else:
                    #         if matched[0] == -1:
                    #             matched[0] = i
                    #         matched[1] = matched[1] + 1

                    currentValues.append((matched[0] - (mapStart-destination), matched[1]))
                    if (unmatched1[1] != 0):
                        prevPartials.append((unmatched1[0], unmatched1[1]))
                    if (unmatched2[1] != 0):
                        prevPartials.append((unmatched2[0], unmatched2[1]))
            
        for unmatched in prevPartials:
            previousValues.append(unmatched)

for prev in previousValues:
    currentValues.append(prev)

print('Values after ' + currentMapping + ': ' + str(currentValues))

lowest = currentValues[0][0]
for val in currentValues:
    if (val[0] < lowest):
        lowest = val[0]

print('Lowest Location: ' + str(lowest))