def printGrid(grid):
    for row in grid:
        print(row)

def process(file):
    return [[int(x) for x in list(l.strip())] for l in open(file).readlines()]

def getVisibilityGrid(grid):
    numRows = len(grid)
    numCols = len(grid[0])
    visible = [[False for t in row] for row in grid]
    for r in range(numRows):
        # left to right
        currMax = -1
        for c in range(numCols):
            if grid[r][c] > currMax:
                visible[r][c] = True
                currMax = grid[r][c]
        # right to left
        currMax = -1
        for c in range(numCols - 1, -1, -1):
            if grid[r][c] > currMax:
                visible[r][c] = True
                currMax = grid[r][c]
    
    for c in range(numCols):
        # top to bottom
        currMax = -1
        for r in range(numRows):
            if grid[r][c] > currMax:
                visible[r][c] = True
                currMax = grid[r][c]
        # bottom to top
        currMax = -1
        for r in range(numRows - 1, -1, -1):
            if grid[r][c] > currMax:
                visible[r][c] = True
                currMax = grid[r][c]
    return visible

def countVisible(visibleGrid):
    return sum([sum(row) for row in visibleGrid])

def getScenicScore(grid, row, col):
    numRows = len(grid)
    numCols = len(grid[0])
    tree = grid[row][col]
    score = 1
    # look right
    count = 0
    for c in range(col + 1, numCols):
        count += 1
        if grid[row][c] >= tree:
            break
    score *= count
    # look left
    count = 0
    for c in range(col - 1, -1, -1):
        count += 1
        if grid[row][c] >= tree:
            break
    score *= count
    # look down
    count = 0
    for r in range(row + 1, numRows):
        count += 1
        if grid[r][col] >= tree:
            break
    score *= count 
    # look up
    count = 0
    for r in range(row - 1, -1, -1):
        count += 1
        if grid[r][col] >= tree:
            break
    score *= count
    return score

def getBestScenicScore(grid):
    numRows = len(grid)
    numCols = len(grid[0])
    bestScenicScore = 0
    for r in range(numRows):
        for c in range(numCols):
            scenicScore = getScenicScore(grid, r, c)
            bestScenicScore = max(bestScenicScore, scenicScore)
    return bestScenicScore

def solvePart1(grid):
    return countVisible(getVisibilityGrid(grid))

def solvePart2(grid):
    return getBestScenicScore(grid)

def solve(file):
    grid = process(file)
    print(f"Part 1: {solvePart1(grid)}")
    print(f"Part 2: {solvePart2(grid)}")

solve("inputs/08/full.txt")
