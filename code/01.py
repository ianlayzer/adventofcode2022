# part 1
def getMostCalories(lines):
    maxCount = 0
    currCount = 0
    for l in lines:
        if l == '':
            maxCount = max(maxCount, currCount)
            currCount = 0
        else:
            currCount += int(l)
    maxCount = max(maxCount, currCount)
    return maxCount

# part 2
def getCalorieCounts(lines):
    elves = []
    currElf = 0
    for l in lines:
        if l == '':
            elves.append(currElf)
            currElf = 0
        else:
            currElf += int(l)
    elves.append(currElf)
    return elves

def getTotalOfTopNElves(lines, n):
    elves = getCalorieCounts(lines)
    elvesSorted = sorted(elves, reverse=True)
    return sum(elvesSorted[:n])

def solve(file):
    lines = [l.strip() for l in open(file).readlines()]
    mostCalories = getMostCalories(lines)
    print(f"Most calories: {mostCalories}")
    top3Elves = getTotalOfTopNElves(lines, 3)
    print(f"Sum of top 3 elves: {top3Elves}")
solve("inputs/01/full.txt")