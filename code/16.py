from collections import defaultdict
from functools import reduce

class Valve:
    def __init__(self, id, flowRate, neighbors):
        self.id = id
        self.flowRate = flowRate
        self.neighbors = neighbors

    def __repr__(self):
        return f"Valve(id={self.id}, flowRate={self.flowRate})"

class State:
    def __init__(self, currTime, currPressure, meValve, elValve, myTurn, activatedValves):
        self.currTime = currTime
        self.currPressure = currPressure
        self.meValve = meValve
        self.elValve = elValve
        self.myTurn = myTurn
        self.activatedValves = activatedValves

    def __repr__(self):
        return f"time:{self.currTime}, pressure:{self.currPressure}, me:{self.meValve.id},el:{self.elValve.id},turn:{self.myTurn},currTime:{self.currTime},activatedValves:{str(self.activatedValves)}"

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


def maximizePressureWithElephant(valves, totalTime):
    CUTOFF = 500000
    idToValve = {}
    for valve in valves:
        idToValve[valve.id] = valve

    def getNextStates(state):
        nextStates = set()
        if state.myTurn:
            currValve = state.meValve
            newTime = state.currTime
        else:
            currValve = state.elValve
            newTime = state.currTime + 1

        # open current valve
        if currValve.flowRate > 0 and currValve.id not in state.activatedValves:
            newPressure = state.currPressure + (totalTime - state.currTime) * currValve.flowRate
            newActivatedValves = state.activatedValves.copy()
            newActivatedValves.add(currValve.id)
            nextStates.add(State(newTime, newPressure, state.meValve, state.elValve, not state.myTurn, newActivatedValves))
        # travel to new valves
        for neighborId in currValve.neighbors:
            neighborValve = idToValve[neighborId]
            if state.myTurn:
                newMeValve = neighborValve
                newElValve = state.elValve
            else:
                newMeValve = state.meValve
                newElValve = neighborValve 
            nextStates.add(State(newTime, state.currPressure, newMeValve, newElValve, not state.myTurn, state.activatedValves.copy()))
        return nextStates

    currStates = set([State(1, 0, idToValve["AA"], idToValve["AA"], True, set())])
    while next(iter(currStates)).currTime < totalTime:
        print(next(iter(currStates)).currTime)
        nextStates = set()
        for currState in currStates:
            for nextState in getNextStates(currState):
                nextStates.add(nextState) 
        currStates = sorted(list(nextStates), key=lambda s:s.currPressure, reverse=True)[:CUTOFF]
    
    return max(map(lambda s: s.currPressure, currStates))

def solve(file):
    valves = parse(file)
    # print(f"Part 1: {maximizePressure(valves, 30)}")
    print(f"Part 2: {maximizePressureWithElephant(valves, 26)}")

solve("inputs/16/full.txt")
