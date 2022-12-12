from collections import deque

class Grid:
    def __init__(self, grid):
        self.grid = grid
        self.numRows = len(grid)
        self.numCols = len(grid[0])
    
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
            cR, cC = currPos
            dR, dC = destPos 
            return ord(self.grid[dR][dC]) - ord(self.grid[cR][cC]) <= 1

        r, c = currPos
        neighbors = [(r, c - 1), (r + 1, c), (r, c + 1), (r - 1, c)]
        neighbors = filter(isInRange, neighbors)
        return list(filter(lambda n: isReachable(currPos, n), neighbors))       

    def print(self):
        for row in self.grid:
            print(row)

def process(file):
    return Grid([list(l.strip()) for l in open(file).readlines()])

def findShortestPath(grid):
    startPos = grid.findSquare("S")
    endPos = grid.findSquare("E")
    grid.setSquare(startPos, "a")
    grid.setSquare(endPos, "z")
    parents = {}
    visited = set()
    frontier = deque([(startPos, None)])
    while len(frontier):
        currPos, prevPos = frontier.popleft()
        if currPos in visited:
            continue
        visited.add(currPos)
        parents[currPos] = prevPos
        if currPos == endPos:
            break
        for neighbor in grid.getNeighbors(currPos):
            if neighbor not in visited:
                frontier.append((neighbor, currPos))
    path = []
    currPos = endPos
    while currPos:
        path.append(currPos)
        currPos = parents[currPos]
    return path[::-1]

def solve(file):
    grid = process(file)
    shortestPath = findShortestPath(grid)
    print(f"Part 1: {len(shortestPath) - 1}")
    
solve("inputs/12/full.txt")
