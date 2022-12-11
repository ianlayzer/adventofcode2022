import operator
from functools import reduce

class Monkey:
    def __init__(self, id, startingItems, operation, testCondn, testConsq, testAltrn, monkeyMap):
        self.id = id
        self.items = startingItems
        self.operation = operation
        self.testCondn = testCondn
        self.testConsq = testConsq
        self.testAltrn = testAltrn
        self.monkeyMap = monkeyMap
        self.inspectionCount = 0
    
    def inspectItems(self):
        # print(f"Monkey {self.id}")
        for item in self.items:
            # print(f"  Monkey inspects an item with a worry level of {item}")
            item = self.operation(item)
            # print(f"    Worry level increases to {item}")
            item = item // 3
            # print(f"    Monkey gets nbored with item. Worry level is divided by 3 to {item}")
            self.inspectionCount += 1
            if item % self.testCondn == 0:
                # print(f"    Current worry level is divisible by {self.testCondn}")
                recipient = self.testConsq
            else:
                # print(f"    Current worry level is not divisible by {self.testCondn}")
                recipient = self.testAltrn
            # print(f"    Item with worry level {item} is thrown to monkey {recipient}")
            self.monkeyMap[recipient].acceptItem(item)
        self.items = []

    def acceptItem(self, item):
        self.items.append(item)

    def reportState(self):
        itemString = ", ".join(map(lambda n: str(n), self.items))
        print(f"Monkey {self.id}: {itemString}")

def parseOperation(opString):
    opString = opString.replace("new = ", "")
    if "*" in opString:
        splt = opString.split(" * ")
        op = operator.mul
    else:
        splt = opString.split(" + ")
        op = operator.add
    if splt[1] == "old":
        return lambda old: op(old, old)
    else:
        return lambda old: op(old, int(splt[1]))

def process(file):
    lines = [l.strip() for l in open(file).readlines()]
    monkeyMap = {}
    l = 0
    while l < len(lines):
        id = lines[l].replace("Monkey ", "").replace(":", "")
        startingItems = list(map(lambda s: int(s), lines[l + 1].replace("Starting items: ", "").split(", ")))
        operation = parseOperation(lines[l + 2].replace("Operation: ", ""))
        testCondn = int(lines[l + 3].replace("Test: divisible by ", ""))
        testConsq = lines[l + 4].replace("If true: throw to monkey ", "")
        testAltrn = lines[l + 5].replace("If false: throw to monkey ", "")
        monkey = Monkey(id, startingItems, operation, testCondn, testConsq, testAltrn, monkeyMap)
        monkeyMap[monkey.id] = monkey
        l += 7
    return monkeyMap

def calculateMonkeyBusiness(monkeys):
    return reduce(operator.mul, sorted(map(lambda m: m.inspectionCount, monkeys), reverse=True)[:2], 1)

def simulateRounds(monkeys, numRounds):
    for r in range(1, numRounds + 1):
        for monkey in monkeys.values():
            monkey.inspectItems()

        # print(f"After round {r}, the monkeys are holding items with these worry levels")
        # for monkey in monkeys.values():
        #     monkey.reportState()
    return calculateMonkeyBusiness(monkeys.values())

def solve(file):
    monkeys = process(file)
    print(f"Part 1: {simulateRounds(monkeys, 20)}")

solve("inputs/11/small.txt")
