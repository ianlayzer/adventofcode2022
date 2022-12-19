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
    def __init__(self, chamber):
        self.chamber = chamber
        self.currRow, self.currCol = ROCK_START_POS
        self.height = 1
    
    def goDown(self):
        for c in range(self.currCol, self.currCol + 4):
            if not checkIfAir(self.chamber, self.currRow + 1, c):
                return False
        self.currRow += 1
        return True
    
    def goLeft(self):
        if not checkIfAir(self.chamber, self.currRow, self.currCol - 1):
            return False
        self.currCol -= 1
        return True

    def goRight(self):
        if not checkIfAir(self.chamber, self.currRow, self.currCol + 4):
            return False
        self.currCol += 1
        return True

    def fill(self, char):
        for c in range(self.currCol, self.currCol + 4):
            self.chamber[self.currRow][c] = char

class PlusRock:
    def __init__(self, chamber):
        self.chamber = chamber
        self.currRow, self.currCol = ROCK_START_POS
        self.height = 3

    def goDown(self):
        if not checkIfAir(self.chamber, self.currRow + 3, self.currCol + 1):
            return False
        self.currRow += 1
        return True
    
    def goLeft(self):
        if not checkIfAir(self.chamber, self.currRow + 1, self.currCol - 1):
            return False
        self.currCol -= 1
        return True

    def goRight(self):
        if not checkIfAir(self.chamber, self.currRow + 1, self.currCol + 1):
            return False
        self.currCol += 1
        return True

    def fill(self, char):
        self.chamber[self.currRow][self.currCol + 1] = char
        self.chamber[self.currRow + 1][self.currCol] = char
        self.chamber[self.currRow + 1][self.currCol + 1] = char
        self.chamber[self.currRow + 1][self.currCol + 2] = char
        self.chamber[self.currRow + 2][self.currCol + 1] = char

class LRock:
    def __init__(self, chamber):
        self.chamber = chamber
        self.currRow, self.currCol = ROCK_START_POS
        self.height = 3

    def goDown(self):
        for c in range(self.currCol, self.currCol + 3):
            if not checkIfAir(self.chamber, self.currRow + 3, c):
                return False
        self.currRow += 1
        return True
    
    def goLeft(self):
        if not checkIfAir(self.chamber, self.currRow + 2, self.currCol - 1):
            return False
        self.currCol -= 1
        return True

    def goRight(self):
        for r in range(self.currRow, self.currRow + 3):
            if not checkIfAir(self.chamber, r, self.currCol + 1):
                return False
        self.currCol += 1
        return True

    def fill(self, char):
        for c in range(self.currCol, self.currCol + 3):
            self.chamber[self.currRow + 2][c] = char
        for r in range(self.currRow, self.currRow + 3):
            self.chamber[r][self.currCol + 2] = char

class ThinRock:
    def __init__(self, chamber):
        self.chamber = chamber
        self.currRow, self.currCol = ROCK_START_POS
        self.height = 4
    
    def goDown(self):
        if not checkIfAir(self.chamber, self.currRow + 4, self.currCol):
            return False
        self.currRow += 1
        return True
    
    def goLeft(self):
        for r in range(self.currRow, self.currRow + 4):
            if not checkIfAir(self.chamber, r, self.currCol - 1):
                return False
        self.currCol -= 1
        return True

    def goRight(self):
        for r in range(self.currRow, self.currRow + 4):
            if not checkIfAir(self.chamber, r, self.currCol + 1):
                return False
        self.currCol += 1
        return True

    def fill(self, char):
        for r in range(self.currRow, self.currRow + 4):
            self.chamber[r][self.currCol] = char

class SquareRock:
    def __init__(self, chamber):
        self.chamber = chamber
        self.currRow, self.currCol = ROCK_START_POS
        self.height = 2
    
    def goDown(self):
        for c in range(self.currCol, self.currCol + 2):
            if not checkIfAir(self.chamber, self.currRow + 2, c):
                return False
        self.currRow += 1
        return True
    
    def goLeft(self):
        for r in range(self.currRow, self.currRow + 2):
            if not checkIfAir(self.chamber, r, self.currCol - 1):
                return False
        self.currRow -= 1
        return True

    def goRight(self):
        for r in range(self.currRow, self.currRow + 2):
            if not checkIfAir(self.chamber, r, self.currCol + 1):
                return False
        self.currRow += 1
        return True

    def fill(self, char):
        for r in range(self.currRow, self.currRow + 2):
            for c in range(self.currCol, self.currCol + 2):
                self.chamber[r][c] = char

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
        rk.fill("@")
        printChamber(chamber)
        rk.fill(".")

    topRock = float('inf')
    for r in range(numRocks):
        rock = ROCK_CLASSES[r % 5](chamber)
        heightIncreaseNeeded = rock.height + 4 - topRock
        
        printCurr(rock)
        jetIndex = 0
        isFalling = True
        while isFalling:
            jet = jets[jetIndex]
            if jet == LEFT:
                rock.goLeft()
            elif jet == RIGHT:
                rock.goRight()
            printCurr(rock) 
            isFalling = rock.goDown()
            printCurr(rock)
            jetIndex += 1
        topRock = min(topRock, rock.currRow)
        print(topRock)
        rock.fill(ROCK)
        printChamber(chamber)

    printChamber(chamber)
    return 0

def solve(file):
    jets = parse(file)
    print(f"Part 1: {simulateRocks(jets, 2)}")

solve("inputs/17/small.txt")
