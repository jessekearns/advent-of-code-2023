from pathlib import Path

class Lens:
    def __init__(self, label, focalLength): 
        self.label = label
        self.focalLength = focalLength

def Hash(input):
    curr = 0
    for c in input:
        curr = curr + ord(c)
        curr = curr * 17
        curr = curr % 256
    return curr

inputfile = Path(__file__).parent / "input.txt"
with open(inputfile) as f:
    lines = f.readlines()
if len(lines) > 1:
    print("Input issue! Check formatting")

lensBoxes = dict()
for i in range (0, 255):
    lensBoxes[i] = []
hashSum = 0

for input in lines[0].replace('\n', '').split(','):
    hashSum = hashSum + Hash(input)
    if '-' in input:
        hashValue = Hash(input[:-1])
        for i in range(0, len(lensBoxes[hashValue])):
            if lensBoxes[hashValue][i].label == input[:-1]:
                del(lensBoxes[hashValue][i])
                break
    elif '=' in input:
        segments = input.split('=')
        label = segments[0]
        focalLength = int(segments[1])
        hashValue = Hash(label)
        existingLensReplaced = False
        for i in range(0, len(lensBoxes[hashValue])):
            if lensBoxes[hashValue][i].label == label:
                lensBoxes[hashValue][i].focalLength = focalLength
                existingLensReplaced = True
                break
        if existingLensReplaced == False:
            lensBoxes[hashValue].append(Lens(label, focalLength))

focusingPower = 0
for i in range(0, 255):
    debugString = str(i) + ': ' 
    for j in range(0, len(lensBoxes[i])):
        focusingPower = focusingPower + lensBoxes[i][j].focalLength * (j + 1) * (i + 1)
        debugString = debugString + str(lensBoxes[i][j].label) + ' ' + str(lensBoxes[i][j].focalLength) + ','
    # if (len(lensBoxes[i]) > 0):
    #     print(debugString)



print('Hash Sum: ' + str(hashSum))
print('Focusing Power: ' + str(focusingPower))