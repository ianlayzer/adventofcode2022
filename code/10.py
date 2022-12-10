def process(file):
    return [l.strip() for l in open(file).readlines()]

def recordSignalStrengths(operations, cycleNumbersToRecord):
    signalStrengths = []
    cycleNumber = 1
    registerValue = 1
    for op in operations:
        if cycleNumber in cycleNumbersToRecord:
            signalStrengths.append(cycleNumber * registerValue)
        if op == "noop":
            cycleNumber += 1
        else:
            cycleNumber += 1
            if cycleNumber in cycleNumbersToRecord:
                signalStrengths.append(cycleNumber * registerValue)
            registerValue += int(op.split(" ")[1])
            cycleNumber += 1
    return signalStrengths

def drawScreen(operations, width, height):
    screen = [['.' for _ in range(width)] for _ in range(height)]
    def getPixelCoords(cycleNumber):
        return (cycleNumber - 1) // width, (cycleNumber - 1) % width
    def drawPixel(pixelRow, pixelCol, registerValue):
        middle = registerValue % width
        if pixelCol >= (middle - 1) and pixelCol <= (middle + 1):
            screen[pixelRow][pixelCol] = "#"

    cycleNumber = 1
    registerValue = 1
    for op in operations:
        pixelRow, pixelCol = getPixelCoords(cycleNumber)
        drawPixel(pixelRow, pixelCol, registerValue)
        if op == "noop":
            cycleNumber += 1
        else:
            cycleNumber += 1
            pixelRow, pixelCol = getPixelCoords(cycleNumber)
            drawPixel(pixelRow, pixelCol, registerValue)
            registerValue += int(op.split(" ")[1])
            cycleNumber += 1
    return screen

def printScreen(screen):
    for row in screen:
        print("".join(row))

def solve(file):
    operations = process(file)
    signalStrengths = recordSignalStrengths(operations, [20, 60, 100, 140, 180, 220])
    print(f"Part 1: {sum(signalStrengths)}")
    print("Part 2:")
    printScreen(drawScreen(operations, 40, 6))

solve("inputs/10/full.txt")
