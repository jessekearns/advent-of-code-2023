from pathlib import Path

inputfile = Path(__file__).parent / "input.txt"
with open(inputfile) as f:
    lines = f.readlines()

timeStrings = lines[0].split(':')[1].strip().split(' ')
distanceStrings = lines[1].split(':')[1].strip().split(' ')

times = []
distances = []
lowerLimits = []
upperLimits = []

for timeString in timeStrings:
    if timeString.isnumeric():
        times.append(int(timeString))

for distString in distanceStrings:
    if distString.isnumeric():
        distances.append(int(distString))

for i in range(0, len(times)):
    raceTime = times[i]
    raceRecord = distances[i]

    lowerLimitFound = False
    upperLimitFound = False

    for j in range(0, raceTime):
        if lowerLimitFound and upperLimitFound:
            break

        thisDistance = j * (raceTime - j)
        if (lowerLimitFound and thisDistance <= raceRecord):
            upperLimits.append(j)
            upperLimitFound = True
        elif (lowerLimitFound == False and thisDistance > raceRecord):
            lowerLimits.append(j)
            lowerLimitFound = True  

product = 1
for k in range(0, len(lowerLimits)):
    numberOfOptions = upperLimits[k] - lowerLimits[k]
    product = product * numberOfOptions

print('Part 1: ' + str(product))

# Part 2
bigRaceLowerLimit = 0
bigRaceUpperLimit = 0

raceTime = 59688274 # 71530
raceRecord = 543102016641022 # 940200

lowerLimitFound = False
upperLimitFound = False

for j in range(0, raceTime):
    if lowerLimitFound and upperLimitFound:
        break

    thisDistance = j * (raceTime - j)
    if (lowerLimitFound and thisDistance <= raceRecord):
        bigRaceUpperLimit = j
        upperLimitFound = True
    elif (lowerLimitFound == False and thisDistance > raceRecord):
        bigRaceLowerLimit = j
        lowerLimitFound = True  

print('Part 2: ' + str(bigRaceUpperLimit - bigRaceLowerLimit))