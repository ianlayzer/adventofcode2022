from collections import deque

class Grid:
    def __init__(self, grid):
        self.grid = grid
        self.numRows = len(grid)
        self.numCols = len(grid[0])
        self.startPos = self.findSquare("S")
        self.endPos = self.findSquare("E")
        self.setSquare(self.startPos, "a")
        self.setSquare(self.endPos, "z")

    def getVal(self, pos):
        return self.grid[pos[0]][pos[1]]
    
    def findSquare(self, val):  
        for r in range(self.numRows):
            for c in range(self.numCols):
                if self.grid[r][c] == val:
                    return r, c
        return None

    def setSquare(self, pos, val):
        self.grid[pos[0]][pos[1]] = val

    def getNeighbors(self, currPos):
        def isInRange(pos):
            r, c = pos
            return r >= 0 and r < self.numRows and c >= 0 and c < self.numCols

        def isReachable(currPos, destPos):
            return ord(self.getVal(destPos)) - ord(self.getVal(currPos)) <= 1

        r, c = currPos
        neighbors = [(r, c - 1), (r + 1, c), (r, c + 1), (r - 1, c)]
        neighbors = filter(isInRange, neighbors)
        return list(filter(lambda n: isReachable(currPos, n), neighbors))       

    def print(self):
        for row in self.grid:
            print(row)

def process(file):
    return Grid([list(l.strip()) for l in open(file).readlines()])

def findShortestPath(grid, startPos):
    parents = {}
    visited = set()
    frontier = deque([(startPos, None)])
    while len(frontier):
        currPos, prevPos = frontier.popleft()
        if currPos in visited:
            continue
        visited.add(currPos)
        parents[currPos] = prevPos
        if currPos == grid.endPos:
            break
        for neighbor in grid.getNeighbors(currPos):
            if neighbor not in visited:
                frontier.append((neighbor, currPos))

    if grid.endPos not in parents:
        return -1
    path = []
    currPos = grid.endPos
    while currPos:
        path.append(currPos)
        currPos = parents[currPos]
    return len(path[::-1]) - 1

def findShortestOfAllPaths(grid):
    shortest = float('inf')
    for r in range(grid.numRows):
        for c in range(grid.numCols):
            pos = r, c
            if grid.getVal(pos) == "a":
                pathLength = findShortestPath(grid, pos)
                if pathLength > 0 and pathLength < shortest:
                    shortest = pathLength
    return shortest

def solve(file):
    grid = process(file)
    print(f"Part 1: {findShortestPath(grid, grid.startPos)}")
    print(f"Part 2: {findShortestOfAllPaths(grid)}")
    
solve("inputs/12/full.txt")
