from pathlib import Path

class SymbolEntry:
    def __init__(self, symbol, index): 
        self.symbol = symbol
        self.index = index
        self.matches = []

    def symbol_matched(self, number):
        self.matches.append(number)

class NumberEntry:
    def __init__(self, number, index): 
        self.number = number
        self.startIndex = index - (len(str(number)) - 1)
        self.endIndex = index
        self.matched = False

    def item_matched(self):
        self.matched = True

def update_count(symbol, count, dictionary):
    if symbol not in dictionary:
        dictionary[symbol] = 0
    dictionary[symbol] = dictionary[symbol] + count

def insert_number(number, index, previousSymbols, currentSymbols, currentNums, dictionary):
    currentNums.append(NumberEntry(number, index))

    # Check if this is immediately after a symbol in the current line
    if len(currentSymbols) > 0 and currentSymbols[-1].index == currentNums[-1].startIndex - 1:
        update_count(currentSymbols[-1].symbol, number, dictionary)
        currentNums[-1].item_matched()
        currentSymbols[-1].symbol_matched(currentNums[-1].number)

    # For each of the previous row's symbols, check if it's in range of being adjacent to this number
    for previousSymbol in previousSymbols:
        if previousSymbol.index <= currentNums[-1].endIndex + 1 and previousSymbol.index >= currentNums[-1].startIndex - 1:
            update_count(previousSymbol.symbol, number, dictionary)
            currentNums[-1].item_matched()
            previousSymbol.symbol_matched(currentNums[-1].number)

def insert_symbol(symbol, index, previousNums, currentNums, currentSymbols, dictionary):
    currentSymbols.append(SymbolEntry(symbol, index))

    # Check if this is immediately after a number in the current line
    if len(currentNums) > 0 and currentNums[-1].endIndex == currentSymbols[-1].index - 1:
        update_count(currentSymbols[-1].symbol, currentNums[-1].number, dictionary)
        currentNums[-1].item_matched()
        currentSymbols[-1].symbol_matched(currentNums[-1].number)

    # For each of the previous row's numbers, check if it's in range of being adjacent to this symbol
    for previousNum in previousNums:
        if index <= previousNum.endIndex + 1 and index >= previousNum.startIndex - 1:
            update_count(symbol, previousNum.number, dictionary)
            previousNum.item_matched()
            currentSymbols[-1].symbol_matched(previousNum.number)

inputfile = Path(__file__).parent / "input.txt"
with open(inputfile) as f:
    lines = f.readlines()

dictionary = dict(unmatched = 0, gearRatios = 0)
previousNums = []
currentNums = []
previousSymbols = []
currentSymbols = []

for line in lines:
    currentNumString = ""

    for i in range(0, len(line)):
        # Skip the edge
        if line[i] == '\n':
            continue

        # If it's a digit, keep scanning until the end of the number
        if line[i].isdigit():
            currentNumString = currentNumString + line[i]
            continue
        
        # Else, record any number that we just finished scanning
        if currentNumString != "":
            insert_number(int(currentNumString), i - 1, previousSymbols, currentSymbols, currentNums, dictionary)
            currentNumString = ""

        # Check if this is a symbol, and record it
        if line[i] != '.':
            insert_symbol(line[i], i, previousNums, currentNums, currentSymbols, dictionary)

    # Check for a number one last time, to handle when it ends at the right edge
    if currentNumString != "":
            insert_number(int(currentNumString), i - 1, previousSymbols, currentSymbols, currentNums, dictionary)
            currentNumString = ""

    # Update the unmatched count
    for previousNum in previousNums:
        if previousNum.matched == False:
            dictionary["unmatched"] = dictionary["unmatched"] + previousNum.number

    # Update gear ratios
    for previousSymbol in previousSymbols:
        if previousSymbol.symbol == '*' and len(previousSymbol.matches) == 2:
            ratio = previousSymbol.matches[0] * previousSymbol.matches[1]
            dictionary["gearRatios"] = dictionary["gearRatios"] + ratio

    previousNums = currentNums
    currentNums = []
    previousSymbols = currentSymbols
    currentSymbols = []

# Update counts one last time to get unmatched counts and gear ratios in the final row
for previousNum in previousNums:
    if previousNum.matched == False:
        dictionary["unmatched"] = dictionary["unmatched"] + previousNum.number

for previousSymbol in previousSymbols:
    if previousSymbol.symbol == '*' and len(previousSymbol.matches) == 2:
        ratio = previousSymbol.matches[0] * previousSymbol.matches[1]
        dictionary["gearRatios"] = dictionary["gearRatios"] + ratio

# Iterate dictionary and get sums
partSum = 0
for key in dictionary:
    print(key + ": " + str(dictionary[key]))
    if (key != "unmatched"):
        partSum = partSum + dictionary[key]

print('Part Sum: ' + str(partSum))