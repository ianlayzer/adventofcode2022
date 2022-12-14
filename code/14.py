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
    def __init__(self, paths):
        self.minX, self.maxX, self.minY, self.maxY = getBounds(paths)
        self.maxY += 2 # for floor
        self.grid = [[AIR for _ in range(self.maxX + 1)] for _ in range(self.maxY + 1)]
        self.height = len(self.grid)
        self.width = len(self.grid[0])
        self.fillRock(paths)
        self.sandX, self.sandY = 500, 0
        self.grid[self.sandY][self.sandX] = "+"
    
    def fillRock(self, paths):
        for path in paths:
            startX, startY = None, None
            for endX, endY in path:
                if startX and startY:
                    for y in range(min(startY, endY), max(startY, endY)+1):
                        for x in range(min(startX, endX), max(startX, endX)+1):
                            self.grid[y][x] = ROCK
                startX, startY = endX, endY
        # fill in floor
        for x in range(self.width):
            self.grid[self.height - 1][x] = ROCK

    def getVal(self, x, y):
        if x >= 0 and x < self.width and y >= 0 and y < self.height:
            return self.grid[y][x]
        else:
            return None

    def simulate(self):
        def dropUnitOfSand():
            # drop grain of sand (sand falls +y)
            currX, currY = self.sandX, self.sandY
            while currY < self.height:
                if self.getVal(currX, currY + 1) == AIR:
                    currY += 1
                elif self.getVal(currX - 1, currY + 1) == AIR:
                    currY += 1
                    currX -= 1
                elif self.getVal(currX + 1, currY + 1) == AIR:
                    currY += 1
                    currX += 1
                else:
                    self.grid[currY][currX] = SAND
                    return (currX, currY)
            return None
        sandCount = 0
        restingPosition = True
        while restingPosition and restingPosition != (self.sandX, self.sandY):
            self.print()
            restingPosition = dropUnitOfSand()
            if restingPosition:
                print(restingPosition)
                self.minX = min(self.minX, restingPosition[0])
                self.maxX = max(self.maxX, restingPosition[0])
                self.minY = min(self.minY, restingPosition[1])
                self.maxY = max(self.maxY, restingPosition[1])
                sandCount += 1
        return sandCount
    
    def print(self):
        for row in self.grid[:self.maxY+1]:
            print("".join(row[self.minX:self.maxX+1]))

def solve(file):
    paths = parse(file)
    grid = Grid(paths)
    print(f"Part 1: {grid.simulate()}")

solve("inputs/14/small.txt")
