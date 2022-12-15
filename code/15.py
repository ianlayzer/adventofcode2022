def getManhattanDistance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def parse(file):
    def parseCoords(coords):
        return tuple(map(lambda s: int(s), coords.split(",")))

    def parseLine(line):
        line = line.replace("Sensor at x=", "") \
                    .replace(" y=", "") \
                    .replace(" closest beacon is at x=", "") \
                    .split(":")
        sensor = parseCoords(line[0])
        beacon = parseCoords(line[1])
        return sensor, beacon, getManhattanDistance(sensor, beacon)

    return [parseLine(l.strip()) for l in open(file).readlines()]

def countImpossiblePositionsInRow(sensorReadings, row):
    impossiblePositions = set()
    for sensor, _, sensorToBeaconDist in sensorReadings:
        sensorX, sensorY = sensor
        sensorToRow = abs(sensorY - row)
        horiz = sensorToBeaconDist - sensorToRow
        for x in range(sensorX - horiz, sensorX + horiz + 1, 1):
            impossiblePositions.add((x, row))
    return len(impossiblePositions) - 1

def findBeaconTuningFrequency(sensorReadings):
    bound = 4000000
    for row in range(bound + 1):
        if row % 10000 == 0:
            print(f"Row {row}/{bound}")
        candidates = set()
        sensorsInRange = set()
        for sensor, _, sensorToBeaconDist in sensorReadings:
            sensorX, sensorY = sensor
            sensorToRow = abs(sensorY - row)
            horiz = sensorToBeaconDist - sensorToRow
            if horiz >= 0:
                sensorsInRange.add((sensor, sensorToBeaconDist))
                candidates.add((sensorX + horiz + 1, row))
                candidates.add((sensorX - horiz - 1, row))
        for cand in candidates:
            if cand[0] < 0 or cand[0] > bound:
                continue
            valid = True
            for sensor, sensorToBeaconDist in sensorsInRange:
                if getManhattanDistance(sensor, cand) <= sensorToBeaconDist:
                    valid = False
                    break
            if valid:
                return cand[0] * bound + cand[1]
        

def solve(file):
    sensorReadings = parse(file)
    print(f"Part 1: {countImpossiblePositionsInRow(sensorReadings, 10)}")
    print(f"Part 2: {findBeaconTuningFrequency(sensorReadings)}")

solve("inputs/15/full.txt")
