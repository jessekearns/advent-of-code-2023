from pathlib import Path

inputfile = Path(__file__).parent / "input.txt"
with open(inputfile) as f:
    lines = f.readlines()

redLimit = 12
greenLimit = 13
blueLimit = 14

currentGame = 1
sum = 0
pwrSum = 0

for game in lines:
    segments = game.split(':')

    gameId = segments[0]
    redMax = 0
    greenMax = 0
    blueMax = 0

    pulls = segments[1].split(';')
    for pull in pulls:
        redPull = 0
        greenPull = 0
        bluePull = 0
        colors = pull.split(',')
        for color in colors:
            elements = color.strip().split(' ')
            if elements[1] == 'red':
                redPull = int(elements[0])
            elif elements[1] == 'green':
                greenPull = int(elements[0])
            elif elements[1] == 'blue':
                bluePull = int(elements[0])
        
        redMax = max(redMax, redPull)
        greenMax = max(greenMax, greenPull)
        blueMax = max(blueMax, bluePull)

    power = redMax * greenMax * blueMax
    pwrSum = pwrSum + power

    if redMax <= redLimit and greenMax <= greenLimit and blueMax <= blueLimit:
        print('Game ' + str(currentGame) + ' is possible')
        sum += currentGame

    else:
        print('Game ' + str(currentGame) + ' is NOT possible')

    currentGame = currentGame + 1

print('ID Sum: ' + str(sum))
print('Power Sum: ' + str(pwrSum))