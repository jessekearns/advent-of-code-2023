from pathlib import Path

inputfile = Path(__file__).parent / "input.txt"
with open(inputfile) as f:
    lines = f.readlines()

values = []
predictions = []
histories = []
velocities = []

i = 0
for line in lines:
    # Parse the input and store it
    segments = line.strip().split(' ')
    currentVals = []
    for seg in segments:
        currentVals.append(int(seg))
    values.append(currentVals)

    # Iterate the velocities until we hit all zeroes
    j = 0
    velocities.append([])
    while len(currentVals) > 1 and any(val != 0 for val in currentVals):
        # print(currentVals)
        newVals = []
        for k in range(0, len(currentVals) - 1):
            newVals.append(currentVals[k+1] - currentVals[k])
        velocities[i].append(newVals)
        j = j + 1
        currentVals = newVals
    # print(currentVals)

    # All zeroes found - iterate back through the velocities until we arrive at our prediction
    currentPrediction = 0
    currentHistory = 0
    while j > 0:
        currentPrediction = currentPrediction + velocities[i][j-1][-1]
        currentHistory = velocities[i][j-1][0] - currentHistory
        j = j-1
    predictions.append(currentPrediction + values[-1][-1])
    histories.append(values[-1][0] - currentHistory)
    # print('---')
    i = i + 1

# print(predictions)
print('Prediction sum: ' + str(sum(predictions)))
# print(histories)
print('Histories sum: ' + str(sum(histories)))