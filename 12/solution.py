from pathlib import Path

def CountValidPatterns(input, numbers):
    if '?' in input:
        for i in range(0, len(input)):
             if input[i] == '?':
                  return CountValidPatterns(input[:i] + '.' + input[i + 1:], numbers) + CountValidPatterns(input[:i] + '#' + input[i + 1:], numbers)
    else:
        currentCount = 0
        resultingCounts = []
        for c in input:
            if c == '#':
                currentCount = currentCount + 1
            else:
                if currentCount > 0:
                    resultingCounts.append(currentCount)
                currentCount = 0
        if currentCount > 0:
                    resultingCounts.append(currentCount)

        if resultingCounts == numbers:
             return 1
        else:
             return 0

inputfile = Path(__file__).parent / "input.txt"
with open(inputfile) as f:
    lines = f.readlines()

isFolded = True
sum = 0

for line in lines:
    segments = line.split(' ')
    nums = []
    for numString in segments[1].replace('\n', '').split(','):
         nums.append(int(numString))

    input = segments[0]
    if isFolded:
         input = segments[0] + '?' + segments[0] + '?' + segments[0] + '?' + segments[0] + '?' + segments[0]
         newNums = nums + nums + nums + nums + nums
         nums = newNums
    configurations = CountValidPatterns(input, nums)

    sum = sum + configurations
    print(input + ' ' + str(nums) + ' ' + str(configurations))

print('Sum: ' + str(sum))