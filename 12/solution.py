from pathlib import Path
import copy

def MemoizedCountValidPatterns(input, numbers, dictionary):
    key = input + '|' + ' '.join(str(n) for n in numbers)
    if key in dictionary:
        return dictionary[key]
    val = CountValidPatterns(input, numbers, dictionary)
    dictionary[key] = val
    reverseKey = input[::-1] + '|' + ' '.join(str(n) for n in reversed(numbers))
    dictionary[reverseKey] = val
    return val

def CountValidPatterns(input, numbers, dictionary):
    # Base case = no more groups to discover
    if len(numbers) == 0:
        if '#' in input:
               return 0
        else:
               return 1
        
    if len(numbers) == 1:
        if len(input) < numbers[0]:
            return 0
        
        firstIndex = input.find('#')
        lastIndex = input.rfind('#')       

        # One number but no # to limit the location: iterate over the segment with a sliding window and increment every valid configuration
        if firstIndex == -1:
            firstPossible = input.find('?')
            lastPossible = input.rfind('?')
            if 1 + lastPossible - firstPossible < numbers[0]:
                return 0
            
            possibilities = 0
            start = firstPossible
            end = firstPossible - 1
            while end < lastPossible:
                end = end + 1
                # End possible continuous segment, restart the sliding window
                if input[end] == '.':
                    start = end + 1
                    continue
                # Still in a contiguous window; check if this is a valid placement and update counter and start index
                if (end - start + 1) == numbers[0]:
                    possibilities = possibilities + 1
                    start = start + 1
            return possibilities
            
        # One number, and at least one # to limit the location: check for validity and return the number of possible placements
        else:
            existingSegmentLength = lastIndex - firstIndex + 1
            if existingSegmentLength > numbers[0]:
                return 0
            for i in range(firstIndex, lastIndex):
                    if input[i] == '.':
                        return 0
            remainingCount = numbers[0] - existingSegmentLength
            leftMargin = 0
            for i in range(1, remainingCount + 1):
                if firstIndex - i >= 0 and input[firstIndex - i] != '.':
                    leftMargin = leftMargin + 1
                else:
                    break

            rightMargin = 0
            for i in range(1, remainingCount + 1):
                if lastIndex + i < len(input) and input[lastIndex + i] != '.':
                    rightMargin = rightMargin + 1
                else:
                    break
            
            if (leftMargin + rightMargin) < remainingCount:
                return 0

            return 1 + (leftMargin + rightMargin) - remainingCount

    # Pick the biggest edge number and multiply the number of valid positions by remaining subproblem solutions
    newInput = input
    newNumbers = copy.deepcopy(numbers)
    if numbers[-1] > numbers[0]:
        newInput = newInput[::-1]
        newNumbers.reverse()

    remainderMinSize = sum(newNumbers) - newNumbers[0] + len(newNumbers) - 1
    lastSegmentEnd = len(newInput) - 1
    while lastSegmentEnd >= 0 and newInput[lastSegmentEnd] == '.':
        lastSegmentEnd = lastSegmentEnd - 1
    lastSegmentStart = 1 + lastSegmentEnd - remainderMinSize
    
    possibilities = 0
    firstPossible = 0
    while firstPossible < len(newInput) and newInput[firstPossible] == '.':
        firstPossible = firstPossible + 1
    start = firstPossible
    end = start - 1
    while end < lastSegmentStart and '#' not in newInput[firstPossible:start]:
        end = end + 1
        # End possible continuous segment, restart the sliding window
        if newInput[end+1:] == '#':
            start = end + 1
            continue
        # Still in a contiguous window; if this is a valid placement for the current number, get the product of recursive subproblems
        if (end - start + 1) == newNumbers[0]:
            if newInput[end + 1] == '#':
                start = start + 1
            else:
                currentPossibilities = MemoizedCountValidPatterns(newInput[start:end+1], [newNumbers[0]], dictionary)
                currentPossibilities = currentPossibilities * MemoizedCountValidPatterns(newInput[end+2:lastSegmentEnd+1], newNumbers[1:], dictionary)
                possibilities = possibilities + currentPossibilities
                start = start + 1
    return possibilities


# Old/Slow
def OldCountValidPatterns(input, numbers):
    if '?' in input:
        for i in range(0, len(input)):
            if input[i] == '?':
                return OldCountValidPatterns(input[:i] + '.' + input[i + 1:], numbers) + OldCountValidPatterns(input[:i] + '#' + input[i + 1:], numbers)
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

isFolded = True # Part 1 vs Part 2
total = 0

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
    configurations = CountValidPatterns(input, nums, dict())
    # oldConfigurations = OldCountValidPatterns(input, nums)
    # if configurations != oldConfigurations:
    #     print(input + ' ' + str(nums) + ' ' + str(configurations))
    #     print('should be '+ str(oldConfigurations))
    #     break

    print(input + ' ' + str(nums) + ' ' + str(configurations))
    total = total + configurations
    

print('Sum: ' + str(total))