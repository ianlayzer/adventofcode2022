def process(file):
    return [(d, int(n)) for (d, n) in [l.strip().split(" ") for l in open(file).readlines()]]

def incrementHead(headPosition, dir):
    headX, headY = headPosition
    if dir == 'R':
        incX, incY = 1, 0
    elif dir == 'D':
        incX, incY = 0, -1
    elif dir == 'L':
        incX, incY = -1, 0
    elif dir == 'U':
        incX, incY = 0, 1
    else:
        raise Exception("Unknown direction")
    return headX + incX, headY + incY

def catchUp(headPosition, tailPosition):
    headX, headY = headPosition
    tailX, tailY = tailPosition
    diffX = headX - tailX
    diffY = headY - tailY
    absDiffX = abs(diffX)
    absDiffY = abs(diffY)
    if absDiffX <= 1 and absDiffY <= 1:
        incX, incY = 0, 0
    elif absDiffX == 2 and absDiffY <= 1:
        incX, incY = diffX // 2, diffY
    elif absDiffX <= 1 and absDiffY == 2:
        incX, incY = diffX, diffY // 2
    elif absDiffX == 2 and absDiffY == 2:
        incX, incY = diffX // 2, diffY // 2
    else:
        raise Exception(f"K2 too far behind K1, k1: {headPosition} k2: {tailPosition}")
    return tailX + incX, tailY + incY

def simulateMotions(motions, numKnots):
    startPosition = (0, 0)
    positions = [startPosition for _ in range(numKnots)]
    tailVisited = set([startPosition])
    for dir, amount in motions:
        for _ in range(amount):
            for k in range(numKnots):
                if k == 0:
                    positions[k] = incrementHead(positions[k], dir)
                else:
                    positions[k] = catchUp(positions[k-1], positions[k])
                    if k == numKnots - 1:
                        tailVisited.add(positions[k])
    return tailVisited

def solve(file):
    motions = process(file)
    print(f"Part 1: {len(simulateMotions(motions, 2))}")
    print(f"Part 2: {len(simulateMotions(motions, 10))}")

solve("inputs/09/full.txt")
