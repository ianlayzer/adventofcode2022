from collections import defaultdict

class Valve:
    def __init__(self, id, flowRate, neighbors):
        self.id = id
        self.flowRate = flowRate
        self.neighbors = neighbors

    def __repr__(self):
        return f"Valve(id={self.id}, flowRate={self.flowRate})"

def parse(file):
    def parseLine(line):
        line = line.replace("Valve ", "") \
                   .replace("has flow rate=", "") \
                   .replace(" tunnels lead to valves ", "") \
                   .replace(" tunnel leads to valve ", "")
        splt = line.split(";")
        left = splt[0].split(" ")
        valveId = left[0]
        flowRate = int(left[1])
        tunnels = splt[1].split(", ")
        return Valve(valveId, flowRate, tunnels)
    return [parseLine(l.strip()) for l in open(file).readlines()]


# class State:
#     def __init__(self, meValve, elephantValve, turn, currTime, activatedValves):
#         self.meValve = meValve
#         self.elephantValve = elephantValve
#         self.turn = turn
#         self.currTime = currTime
#         self.activatedValves = activatedValves

#     def __repr__(self):
#         return f"me:{self.meValve.id},eleph:{self.elephantValve.id},turn:{self.turn},currTime:{self.currTime},activatedValves:{str(self.activatedValves)}"

# class Game:
#     def __init__(self, valves):
#         self.idToValve = {}
#         for valve in valves:
#             self.idToValve[valve.id] = valve
#         self.currentState = State(self.idToValve["AA"], self.idToValve["AA"], True, 1, set())

def maximizePressureWithElephant(valves, totalTime):
    idToValve = {}
    for valve in valves:
        idToValve[valve.id] = valve

    def search2(me, eleph, myTurn, currTime, activatedValves, mem):
            if currTime == totalTime:
                return 0

            stateString = f"me:{me.id},eleph:{eleph.id},myTurn:{myTurn},currTime:{currTime},activatedValves:{str(activatedValves)}"
            if stateString in mem:
                return mem[stateString]

            myBestPressure = 0
            elephBestPressure = 0
            if myTurn:
                if me.id not in activatedValves and me.flowRate > 0:
                    pressureFromCurr = (totalTime - currTime) * me.flowRate
                    activatedValves.add(me.id)
                    myBestPressure = max(myBestPressure, pressureFromCurr + search2(me, eleph, False, currTime, activatedValves, mem))
                    activatedValves.remove(me.id)
                for neighborId in me.neighbors:
                    neighbor = idToValve[neighborId]
                    myBestPressure = max(myBestPressure, search2(neighbor, eleph, False, currTime, activatedValves, mem))
                
            else:
                if eleph.id not in activatedValves and eleph.flowRate > 0:
                    pressureFromCurr = (totalTime - currTime) * eleph.flowRate
                    activatedValves.add(eleph.id)
                    elephBestPressure = max(elephBestPressure,  pressureFromCurr + search2(me, eleph, True, currTime + 1, activatedValves, mem))
                    activatedValves.remove(eleph.id)                
                for neighborId in eleph.neighbors:
                    neighbor = idToValve[neighborId]
                    elephBestPressure = max(elephBestPressure, search2(me, neighbor, True, currTime + 1, activatedValves, mem))
            
            
            bestPressure = myBestPressure + elephBestPressure
            mem[stateString] = bestPressure
            return bestPressure   

    return search2(idToValve["AA"], idToValve["AA"], True, 1, set(), {}) 

def maximizePressure(valves, totalTime):
    idToValve = {}
    for valve in valves:
        idToValve[valve.id] = valve

    def search(currValve, currTime, activatedValves, mem):
        if currTime == totalTime or len(activatedValves) == len(valves):
            return 0
        activatedValvesStr = str(activatedValves)
        if activatedValvesStr in mem:
            return mem[currValve.id][currTime][activatedValvesStr]
        bestPressure = 0
        for neighborId in currValve.neighbors:
            neighborValve = idToValve[neighborId]
            bestPressure = max(bestPressure, search(neighborValve, currTime + 1, activatedValves, mem))
        
        if currValve not in activatedValves and currValve.flowRate > 0:
            pressureFromCurr = (totalTime - currTime) * currValve.flowRate
            activatedValves.add(currValve)
            bestPressure = max(bestPressure, pressureFromCurr + search(currValve, currTime + 1, activatedValves, mem))
            activatedValves.remove(currValve)
        
        mem[currValve.id][currTime][str(activatedValves)] = bestPressure
        return bestPressure

    return search(idToValve["AA"], 1, set(), defaultdict(lambda: defaultdict(dict)))

def solve(file):
    valves = parse(file)
    # print(f"Part 1: {maximizePressure(valves, 30)}")
    print(f"Part 2: {maximizePressureWithElephant(valves, 26)}")

solve("inputs/16/full.txt")
