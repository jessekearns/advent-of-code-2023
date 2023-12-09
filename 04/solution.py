from pathlib import Path

inputfile = Path(__file__).parent / "input.txt"
with open(inputfile) as f:
    lines = f.readlines()

i = 1
sum = 0
copies = dict()

# Initialize copies counter with one of each card
for line in lines:
    copies[i] = 1
    i = i + 1

i = 1
cards = 0

for line in lines:
    segments = line.split(':')[1].split('|')

    winners = segments[0].strip().split(' ')
    numbers = segments[1].strip().split(' ')

    matches = 0
    points = 0
    for number in numbers:
        if (number == ''):
            continue

        if number in winners:
            matches = matches + 1

    for j in range (1, matches + 1):
        copies[i + j] = copies[i + j] + copies[i]

        if points == 0:
            points = 1
        else:
            points = points * 2

    # print('Card ' + str(i) + ' wins ' + str(points) + ' points')
    sum = sum + points
    cards = cards + copies[i]
    i = i + 1

print('Point Sum: ' + str(sum))
print('Card Sum: ' + str(cards))