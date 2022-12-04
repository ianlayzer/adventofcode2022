def process(file):
    lines = [l.strip() for l in open(file).readlines()]
    return [[[int(s) for s in a.split('-')] for a in l.split(',')] for l in lines]    

def checkContains(range1, range2):
    r1Start, r1End = range1
    r2Start, r2End = range2
    return r1Start <= r2Start and r1End >= r2End

def checkOverlaps(range1, range2):
    r1Start, r1End = range1
    r2Start, _ = range2
    return r1Start <= r2Start and r1End >= r2Start

def countCheck(sectionAssignments, check):
    c = 0
    for range1, range2 in sectionAssignments:
        if check(range1, range2) or check(range2, range1):
            c += 1
    return c

def solve(file):
    sectionAssignments = process(file)
    c1 = countCheck(sectionAssignments, checkContains)
    print(f"Part 1: {c1}")
    c2 = countCheck(sectionAssignments, checkOverlaps)
    print(f"Part 2: {c2}")
    
solve("inputs/04/full.txt")
