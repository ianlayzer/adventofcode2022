from functools import cmp_to_key, reduce
import operator

def parse(file):   
    def parseData(data):
        output = []
        listStack = [output]
        numAcc = ""
        for c in data:
            if c == "[":
                newList = []
                listStack[-1].append(newList)
                listStack.append(newList)
            elif c == "]":
                if len(numAcc):
                    listStack[-1].append(int(numAcc))
                numAcc = ""
                listStack.pop()
            elif c == ",":
                if len(numAcc):
                    listStack[-1].append(int(numAcc))
                numAcc = ""
            elif c != ",":
                numAcc += c
            
        return output.pop()

    lines = [l.strip() for l in open(file).readlines()]
    pairs = []
    for i in range(0, len(lines), 3):
        pairs.append((parseData(lines[i]), parseData(lines[i+1])))
    return pairs

def dataToString(data):
    if isinstance(data, list):
        return "[" + ",".join(map(dataToString, data)) + "]"
    else:
        return str(data)

def printDebug(s):
    # print(s)
    pass

LESS = 1
GREATER = -1
EQUAL = 0

def compare(left, right, leadspace):
    printDebug(f"{leadspace}- Compare {dataToString(left)} vs {dataToString(right)}")
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            printDebug(f"{leadspace}  - Left side is smaller, so inputs are in the right order")
            return LESS
        elif left > right:
            printDebug(f"{leadspace}  - Right side is smaller, so inputs are not in the right order")
            return GREATER
        else:
            return EQUAL
    elif isinstance(left, int) and isinstance(right, list):
        printDebug(f"{leadspace}  - Mixed types; convert left to {dataToString([left])} and retry comparison")
        return compare([left], right, leadspace + "  ")
    elif isinstance(left, list) and isinstance(right, int):
        printDebug(f"{leadspace}  - Mixed types; convert right to {dataToString([right])} and retry comparison")
        return compare(left, [right], leadspace + "  ")
    elif isinstance(left, list) and isinstance(right, list):
        i = 0
        while i < len(left) and i < len(right):
            res = compare(left[i], right[i], leadspace + "  ")
            if res == LESS or res == GREATER:
                return res
            i += 1
        if len(left) < len(right):
            printDebug(f"{leadspace}  - Left side ran out of items, so inputs are in the right order")
            return LESS
        elif len(left) > len(right):
            printDebug(f"{leadspace}  - Right side ran out of items, so inputs are not in the right order")
            return GREATER
        else:
            return EQUAL
    else:
        return None


def countPairsInOrder(pairs):
    indices = []
    for i, (left, right) in enumerate(pairs):
        printDebug(f"\n== Pair {i+1} ==")
        if compare(left, right, "") == LESS:
            indices.append(i + 1)
    return sum(indices)

def getPacketsInOrder(pairs):
    def comparePackets(packet1, packet2):
        return -compare(packet1, packet2, "")
    allPackets = []
    allPackets.append([[2]])
    allPackets.append([[6]])
    for pair in pairs:
        left, right = pair
        allPackets += [left, right]
    return sorted(allPackets, key=cmp_to_key(comparePackets))

def getDecoderKey(pairs):
    dividerPackets = ["[[2]]", "[[6]]"]
    dividerPacketIndices = []
    orderedPackets = getPacketsInOrder(pairs)
    for i, p in enumerate(orderedPackets):
        if dataToString(p) in dividerPackets:
            dividerPacketIndices.append(i + 1)
    return reduce(operator.mul, dividerPacketIndices)

def solve(file):
    pairs = parse(file)
    print(file)
    print(f"Part 1: {countPairsInOrder(pairs)}")
    print(f"Part 2: {getDecoderKey(pairs)}")

solve("inputs/13/small.txt")
solve("inputs/13/full.txt")