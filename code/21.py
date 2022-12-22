from collections import deque
import operator

def parse(file):
    return [(l[0], l[1].split(" ")) for l in [l.strip().split(": ") for l in open(file).readlines()]]

OPERATORS = {
    "+": operator.add,
    "*": operator.mul,
    "-": operator.sub,
    "/": operator.floordiv
}

def solveEquations(equations):
    varMap = {}
    unsolved = deque(equations)
    while len(unsolved):
        currEquation = unsolved.popleft()
        currVar, currVal = currEquation
        if len(currVal) == 1:
            varMap[currVar] = int(currVal[0])
            continue
        leftVar, op, rightVar = currVal
        if leftVar not in varMap or rightVar not in varMap:
            unsolved.append(currEquation)
            continue
        varMap[currVar] = OPERATORS[op](varMap[leftVar], varMap[rightVar])

    return varMap["root"]

def solveEquationsHuman(equations):
    TARGET = "humn"
    varToVal = {}
    for var, val in equations:
        varToVal[var] = val
    def solveForHuman(currVar):
        if currVar == TARGET:
            return currVar
        currVal = varToVal[currVar]
        if len(currVal) == 1:
            return int(currVal[0])
        left = solveForHuman(currVal[0])
        right = solveForHuman(currVal[2])
        op = currVal[1]
        if isinstance(left, int) and isinstance(right, int):
            return OPERATORS[op](left, right)
        else:
            return left, op, right


    rootVal = varToVal["root"]
    finalEquation = (solveForHuman(rootVal[0]), "=", solveForHuman(rootVal[2]))

    if isinstance(finalEquation[0], int):
        acc = finalEquation[0]
        currEquation = finalEquation[2]
    else:
        acc = finalEquation[2]
        currEquation = finalEquation[0]

    while currEquation != TARGET:
        left, op, right = currEquation
        if op == "+":
            if isinstance(right, int):
                acc = acc - right
                currEquation = left
            else:
                acc = acc - left
                currEquation = right
        elif op == "*":
            if isinstance(right, int):
                acc = acc // right
                currEquation = left
            else:
                acc = acc // left
                currEquation = right
        elif op == "/":
            if isinstance(right, int):
                acc = acc * right
                currEquation = left
            else:
                acc = left // acc
                currEquation = right
        elif op == "-":
            if isinstance(right, int):
                acc = acc + right
                currEquation = left
            else:
                acc = -1 * (acc - left)
                currEquation = right
        else:
            raise Exception(f"Op not recognized: {op}")
    return acc

def solve(file):
    equations = parse(file)
    print(f"Part 1: {solveEquations(equations)}")
    print(f"Part 2: {solveEquationsHuman(equations)}")

solve("inputs/21/full.txt")
