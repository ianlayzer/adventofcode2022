scoreMap = {
    'X': 1,
    'Y': 2,
    'Z': 3
}
    
strategyMap = {
    'A': {
        'X': 'Z',
        'Y': 'X',
        'Z': 'Y'
    },
    'B':  {
        'X': 'X',
        'Y': 'Y',
        'Z': 'Z'
    },
    'C':  {
        'X': 'Y',
        'Y': 'Z',
        'Z': 'X'
    }
}


# part 1
def getResultScore(opponent, me):
    if (opponent == 'A' and me == 'X') or (opponent == 'B' and me == 'Y') or (opponent == 'C' and me == 'Z'):
        return 3
    elif (opponent == 'A' and me == 'Y') or (opponent == 'B' and me == 'Z') or (opponent == 'C' and me == 'X'):
        return 6
    else:
        return 0

def getScore(opponent, me):
    return getResultScore(opponent, me) + scoreMap[me]

def getScoreComplex(opponent, me):
    return getScore(opponent, strategyMap[opponent][me])

def computeScore(guide):
    totalScore = 0
    for opponent, me in guide:
        score = getScoreComplex(opponent, me)
        totalScore += score
    return totalScore

def solve(file):
    guide = [l.strip().split(' ') for l in open(file).readlines()]
    totalScore = computeScore(guide)
    print(f"Total Score: {totalScore}")

solve("inputs/02/full.txt")