from collections import defaultdict

def process(file):
    lines = [l for l in open(file).readlines()]

    stacks = {}
    moves = []
    indexToStack = defaultdict(list)
    indexToStackLabel = {}    
    l = 0
    while lines[l] != '\n':
        currLine = list(lines[l])
        inCrate = False
        for i, c in enumerate(currLine):
            if c == ' ' or c == '\n':
                continue
            if inCrate and c != ' ' and c != '\n':
                indexToStack[i].append(c)
                inCrate = False
            elif c == '[':
                inCrate = True
            elif c != ']':
                indexToStackLabel[i] = c
        l += 1
    for index, label in indexToStackLabel.items():
        stacks[label] = indexToStack[index][::-1]

    l += 1
    moveLines = [l.strip() for l in lines[l:]]
    for ml in moveLines:
        mlSplit = ml.split(' ')
        # num crates, from stack, to stack
        moves.append((int(mlSplit[1]), mlSplit[3], mlSplit[5]))
        
    return stacks, moves

def applyMove(stacks, move):
    numCrates, fromStack, toStack = move
    for _ in range(numCrates):
        if len(stacks[fromStack]):
                stacks[toStack].append(stacks[fromStack].pop())

def applyMoveAtOnce(stacks, move):
    numCrates, fromStack, toStack = move
    stacks[toStack] += stacks[fromStack][-numCrates:]
    stacks[fromStack] = stacks[fromStack][:-numCrates]

def getTopCrates(stacks, moves, applyMove):
    for move in moves:
        applyMove(stacks, move)
    toReturn = ''
    for label in sorted(stacks.keys()):
        toReturn += stacks[label][-1]
    return toReturn

def solve(file):
    stacks, moves = process(file)
    topCrates = getTopCrates(stacks, moves, applyMove)
    print(f"Part 1: {topCrates}")
    stacks, moves = process(file)
    topCrates = getTopCrates(stacks, moves, applyMoveAtOnce)
    print(f"Part 2: {topCrates}")
solve("inputs/05/full.txt")
