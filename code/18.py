def parse(file):
    return set([(int(l[0]), int(l[1]), int(l[2])) for l in [l.strip().split(",") for l in open(file).readlines()]])

def getNeighbors(x, y, z):
    return [
        ((x + 1, y, z), "posX"),
        ((x - 1, y, z), "negX"),
        ((x, y + 1, z), "posY"),
        ((x, y - 1, z), "negY"),
        ((x, y, z + 1), "posZ"),
        ((x, y, z - 1), "negZ")
    ]

def computeExternalSurfaceArea(cubes):
    surfaceArea = 0
    for x, y, z in cubes:
        for neighbor, _ in getNeighbors(x, y, z):
            if neighbor not in cubes:
                surfaceArea += 1
    return surfaceArea

def computeInternalSurfaceArea(cubes):
    maxX, maxY, maxZ = 0, 0, 0
    for x, y, z in cubes:
        maxX = max(maxX, x)
        maxY = max(maxY, y)
        maxZ = max(maxZ, z)
    def isInRange(point):
        x, y, z = point
        return x >= -1 and x <= maxX + 2 and y >= -1 and y <= maxY + 2 and z >= -1 and z <= maxZ + 2

    visited = set()
    surfacesSeen = set()
    next = [(0, 0, 0)]
    while len(next):
        curr = next.pop()
        if curr in visited:
            continue
        visited.add(curr)
        currX, currY, currZ = curr
        for neighbor, dir in getNeighbors(currX, currY, currZ):
            if neighbor in cubes:
                surfacesSeen.add((neighbor, dir))
            elif isInRange(neighbor):
                next.append(neighbor)
    return len(surfacesSeen)

def solve(file):
    cubes = parse(file)
    print(f"Part 1: {computeExternalSurfaceArea(cubes)}")
    print(F"Part 2: {computeInternalSurfaceArea(cubes)}")

solve("inputs/18/full.txt")
