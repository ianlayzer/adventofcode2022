def parse(file):
    paths = [l.strip().split(" -> ") for l in open(file).readlines()]
    out = []
    for path in paths:
        p = []
        for c in path:
            c = c.split(",")
            p.append((int(c[0]), int(c[1])))
        out.append(p)
    return out

def getBounds(paths):
    minX = minY = float('inf')
    maxX = maxY = float('-inf')
    for path in paths:
        for x,y in path:
            minX = min(minX, x)
            minY = min(minY, y)
            maxX = max(maxX, x)
            maxY = max(maxY, y)
    return minX, maxX, minY, maxY

AIR = "."
ROCK = "#"
SAND = "o"
class Grid:
    def __init__(self, paths, isFloor):
        self.isFloor = isFloor
        self.minX, self.maxX, self.minY, self.maxY = getBounds(paths)
        self.maxY += 2 # for floor
        self.rockPositions = set()
        self.sandPositions = set()
        self.fillRock(paths)
        self.sandSource = (500, 0)
    
    def fillRock(self, paths):
        for path in paths:
            startX, startY = None, None
            for endX, endY in path:
                if startX and startY:
                    for y in range(min(startY, endY), max(startY, endY)+1):
                        for x in range(min(startX, endX), max(startX, endX)+1):
                            self.rockPositions.add((x, y))
                startX, startY = endX, endY

    def getVal(self, x, y):
        if (x, y) in self.rockPositions or (self.isFloor and y == self.maxY):
            return ROCK
        elif (x, y) in self.sandPositions:
            return SAND
        else:
            return AIR

    def simulate(self):
        def dropUnitOfSand():
            # drop grain of sand (sand falls +y)
            currX, currY = self.sandSource
            while currY < self.maxY:
                if self.getVal(currX, currY + 1) == AIR:
                    currY += 1
                elif self.getVal(currX - 1, currY + 1) == AIR:
                    currY += 1
                    currX -= 1
                elif self.getVal(currX + 1, currY + 1) == AIR:
                    currY += 1
                    currX += 1
                else:
                    self.sandPositions.add((currX, currY))
                    return (currX, currY)
            return None
        sandCount = 0
        restingPosition = True
        while restingPosition and restingPosition != self.sandSource:
            restingPosition = dropUnitOfSand()
            if restingPosition:
                self.minX = min(self.minX, restingPosition[0])
                self.maxX = max(self.maxX, restingPosition[0])
                self.minY = min(self.minY, restingPosition[1])
                self.maxY = max(self.maxY, restingPosition[1])
                sandCount += 1
        return sandCount
    
    def print(self):
        s = ""
        for y in range(self.minY, self.maxY + 1):
            for x in range(self.minX, self.maxX + 1):
                s += self.getVal(x, y)
            s += "\n"
        print(s)

def solve(file):
    print(file)
    paths = parse(file)
    print(f"Part 1: {Grid(paths, False).simulate()}")
    print(f"Part 2: {Grid(paths, True).simulate()}")

solve("inputs/14/small.txt")
solve("inputs/14/full.txt")
