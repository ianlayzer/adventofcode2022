def getPriority(letter):
    ordinal = ord(letter)
    if ordinal >= ord('a'):
        return ord(letter) - ord('a') + 1
    else:
        return ord(letter) - ord('A') + 27

def solvePart1(file):
    lines = [l.strip() for l in open(file).readlines()]
    score = 0
    for bag in lines:
        mid = len(bag)//2
        first = set(list(bag[:mid]))
        second = set(list(bag[mid:]))
        inBoth = first.intersection(second)
        score += getPriority(list(inBoth).pop())
    print(f"Part 1: {score}")

def solvePart2(file):
    bags = [l.strip() for l in open(file).readlines()]
    score = 0
    for i in range(0, len(bags), 3):
        group = bags[i:i+3]
        overlap = set()
        for elf in group:
            if overlap:
                overlap = overlap.intersection(list(elf))
            else:
                overlap = set(list(elf))
        score += getPriority(list(overlap).pop())
    print(f"Part 2: {score}")

solvePart1("inputs/03/full.txt")     
solvePart2("inputs/03/full.txt")