def parse(file):
    return list([l.strip() for l in open(file).readlines()][0])

CHAMBER_WIDTH = 7
ROCK_START_POS = 0, 2
LEFT = "<"
RIGHT = ">"
AIR = "."
ROCK = "#"
FLOOR = "-"

def checkIfAir(chamber, r, c):
    return r >= 0 and r < len(chamber) and c >= 0 and c < len(chamber[0]) and chamber[r][c] == AIR

class MinusRock:
    def __init__(self):
        self.currRow, self.currCol = ROCK_START_POS
        self.height = 1

    def getDownNeighbors(self):
        return [(self.currRow + 1, c) for c in range(self.currCol, self.currCol + 4)]

    def getLeftNeighbors(self):
        return [(self.currRow, self.currCol - 1)]

    def getRightNeighbors(self):
        return [(self.currRow, self.currCol + 4)]

    def getPositions(self):
        return [(self.currRow, c) for c in range(self.currCol, self.currCol + 4)]
    
class PlusRock:
    def __init__(self):
        self.currRow, self.currCol = ROCK_START_POS
        self.height = 3

    def getDownNeighbors(self):
        return [
            (self.currRow + 2, self.currCol),
            (self.currRow + 3, self.currCol + 1),
            (self.currRow + 2, self.currCol + 2)
        ]

    def getLeftNeighbors(self):
        return [
            (self.currRow, self.currCol),
            (self.currRow + 1, self.currCol - 1),
            (self.currRow + 2, self.currCol)
        ]

    def getRightNeighbors(self):
        return [
            (self.currRow, self.currCol + 2),
            (self.currRow + 1, self.currCol + 3),
            (self.currRow + 2, self.currCol + 2)
        ]

    def getPositions(self):
        return [
            (self.currRow, self.currCol + 1),
            (self.currRow + 1, self.currCol),
            (self.currRow + 1, self.currCol + 1),
            (self.currRow + 1, self.currCol + 2),
            (self.currRow + 2, self.currCol + 1),
        ]

class LRock:
    def __init__(self):
        self.currRow, self.currCol = ROCK_START_POS
        self.height = 3

    def getDownNeighbors(self):
        return [(self.currRow + 3, c) for c in range(self.currCol, self.currCol + 3)]

    def getLeftNeighbors(self):
        return [
            (self.currRow, self.currCol + 1),
            (self.currRow + 1, self.currCol + 1),
            (self.currRow + 2, self.currCol - 1),
        ]

    def getRightNeighbors(self):
        return [(r, self.currCol + 3) for r in range(self.currRow, self.currRow + 3)]


    def getPositions(self):
        return [
            (self.currRow, self.currCol + 2),
            (self.currRow + 1, self.currCol + 2),
            (self.currRow + 2, self.currCol),
            (self.currRow + 2, self.currCol + 1),
            (self.currRow + 2, self.currCol + 2),
        ]
class ThinRock:
    def __init__(self):
        self.currRow, self.currCol = ROCK_START_POS
        self.height = 4

    def getDownNeighbors(self):
        return [(self.currRow + 4, self.currCol)]

    def getLeftNeighbors(self):
        return [(r, self.currCol - 1) for r in range(self.currRow, self.currRow + 4)]

    def getRightNeighbors(self):
        return [(r, self.currCol + 1) for r in range(self.currRow, self.currRow + 4)]

    def getPositions(self):
        return [(r, self.currCol) for r in range(self.currRow, self.currRow + 4)]

class SquareRock:
    def __init__(self):
        self.currRow, self.currCol = ROCK_START_POS
        self.height = 2
    
    def getDownNeighbors(self):
        return [(self.currRow + 2, c) for c in range(self.currCol, self.currCol + 2)]

    def getLeftNeighbors(self):
        return [(r, self.currCol - 1) for r in range(self.currRow, self.currRow + 2)]

    def getRightNeighbors(self):
        return [(r, self.currCol + 2) for r in range(self.currRow, self.currRow + 2)]

    def getPositions(self):
        positions = []
        for r in range(self.currRow, self.currRow + 2):
            for c in range(self.currCol, self.currCol + 2):
                positions.append((r, c))
        return positions

def goDown(chamber, rock):
    for r, c in rock.getDownNeighbors():
        if not checkIfAir(chamber, r, c):
            return False
    rock.currRow += 1
    return True

def goLeft(chamber, rock):
    for r, c in rock.getLeftNeighbors():
        if not checkIfAir(chamber, r, c):
            return False
    rock.currCol -= 1
    return True

def goRight(chamber, rock):
    for r, c in rock.getRightNeighbors():
        if not checkIfAir(chamber, r, c):
            return False
    rock.currCol += 1
    return True

def fill(chamber, rock, char):
    for r, c in rock.getPositions():
        chamber[r][c] = char    


ROCK_CLASSES = [MinusRock, PlusRock, LRock, ThinRock, SquareRock]

def printChamber(chamber):
    for i, row in enumerate(chamber):
        joinedRow = "".join(row)
        border = "+" if i == len(chamber) - 1 else "|"
        print(f"{border}{joinedRow}{border}")
    print()

def simulateRocks(jets, numRocks):
    chamber = [[AIR] * CHAMBER_WIDTH for _ in range(4)] + [[FLOOR] * CHAMBER_WIDTH]
    def printCurr(rk):
        fill(chamber, rk, "@")
        printChamber(chamber)
        fill(chamber, rk, ".")

    topRock = float('inf')
    jetIndex = 0
    for r in range(numRocks):
        # print("A new rock begins falling:")
        rock = ROCK_CLASSES[r % 5]()
        heightIncrease = rock.height + 3 - topRock
        if heightIncrease > 0:
            addedAir = [[AIR] * CHAMBER_WIDTH for _ in range(heightIncrease)]
            chamber = addedAir + chamber
            topRock += heightIncrease
        elif heightIncrease != float('-inf'):
            rock.currRow = -heightIncrease

        # printCurr(rock)
        isFalling = True
        while isFalling:
            jet = jets[jetIndex % len(jets)]
            jetIndex += 1
            if jet == LEFT:
                goLeft(chamber, rock)
                # if goLeft(chamber, rock):
                #     print("Jet of gas pushes rock left:")
                # else:
                #     print("Jet of gas pushes rock left, but nothing happens:")
            elif jet == RIGHT:
                goRight(chamber, rock)
                # if goRight(chamber, rock):
                #     print("Jet of gas pushes rock right:")
                # else:
                #     print("jet of gas pushes rock right, but nothing happens:")

            # printCurr(rock) 
            isFalling = goDown(chamber, rock)
            # if isFalling:
            #     print("Rock falls 1 unit:")
            #     printCurr(rock)
        topRock = min(topRock, rock.currRow)
        fill(chamber, rock, ROCK)
        # print("Rock falls 1 unit, causing it to come to rest:")
        # printChamber(chamber)
    print("End Result:")
    printChamber(chamber)
    return len(chamber) - topRock - 1

def solve(file):
    jets = parse(file)
    print(f"Part 1: {simulateRocks(jets, 2022)}")

solve("inputs/17/full.txt")
