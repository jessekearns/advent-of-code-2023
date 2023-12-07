from pathlib import Path
import functools

inputfile = Path(__file__).parent / "input.txt"
with open(inputfile) as f:
    lines = f.readlines()

class Hand:
    def __init__(self, cards, bid): 
        self.cards = cards
        self.bid = bid
        
        type = 0
        cardVals = []

        dictionary = dict()
        for c in self.cards:
            if c.isdigit():
                cardVals.append(int(c))
            elif c == 'T':
                cardVals.append(10)
            elif c == 'J':
                # cardVals.append(11)
                cardVals.append(1)
            elif c == 'Q':
                cardVals.append(12)
            elif c == 'K':
                cardVals.append(13)
            elif c == 'A':
                cardVals.append(14)

            if (c not in dictionary):
                dictionary[c] = 0
            dictionary[c] = dictionary[c] + 1

        # Handle Joker logic for part 2
        if 'J' in dictionary:
            jokerCount = dictionary['J']
            del dictionary['J']

            candidateKey = '1'
            candidateVal = 0
            for item in dictionary.items():
                if item[1] > candidateVal:
                    candidateKey = item[0]
                    candidateVal = item[1]

            if candidateKey == '1': # Handle 'JJJJJ'
                dictionary['A'] = 5
            else:
                dictionary[candidateKey] = dictionary[candidateKey] + jokerCount
            
        if len(dictionary) == 1:
            type = 7 # Five of a kind
        elif len(dictionary) == 5:
            type = 1 # High card
        elif len(dictionary) == 4:
            type = 2 # On Pair
        elif len(dictionary) == 3:
            if 3 in dictionary.values():
                type = 4 # Three of a kind
            else:
                type = 3 # Two pair
        elif len(dictionary) == 2:
            if 1 in dictionary.values():
                type = 6 # Four of a kind
            else:
                type= 5 # Full House

        self.type = type
        self.cardVals = cardVals


    def symbol_matched(self, number):
        self.matches.append(number)

def compareHands(x, y):
    if (x.type != y.type):
        return x.type - y.type
    for i in range(0, 5):
        if (x.cardVals[i] != y.cardVals[i]):
            return x.cardVals[i] - y.cardVals[i]
    return 0
    

# Parse hands
hands = []
for line in lines:
    segments = line.split(' ')
    hands.append(Hand(segments[0], int(segments[1])))

# Sort Hands
hands = sorted(hands, key=functools.cmp_to_key(compareHands))

# Sum hand winnings           
sum = 0
for i in range (0, len(hands)):
    print(hands[i].cards)
    sum = sum + hands[i].bid * (i + 1)

print('Sum: ' + str(sum))