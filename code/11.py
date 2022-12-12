import operator
from functools import reduce

class Monkey:
    def __init__(self, id, startingItems, operation, divisor, divisibleRecipient, notDivisibleRecipient, monkeyMap):
        self.id = id
        self.items = startingItems
        self.operation = operation
        self.divisor = divisor
        self.divisibleRecipient = divisibleRecipient
        self.notDivisibleRecipient = notDivisibleRecipient
        self.monkeyMap = monkeyMap
        self.inspectionCount = 0
        self.ceiling = None
    
    def inspectItems(self):
        # print(f"Monkey {self.id}")
        for item in self.items:
            # print(f"  Monkey inspects an item with a worry level of {item}")
            item = self.operation(item)
            # print(f"    Worry level increases to {item}")
            item = item % self.ceiling
            # print(f"    Monkey gets nbored with item. Worry level is divided by 3 to {item}")
            self.inspectionCount += 1
            if item % self.divisor == 0:
                # print(f"    Current worry level is divisible by {self.divisor}")
                recipient = self.divisibleRecipient
            else:
                # print(f"    Current worry level is not divisible by {self.divisor}")
                recipient = self.notDivisibleRecipient
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
        divisor = int(lines[l + 3].replace("Test: divisible by ", ""))
        divisibleRecipient = lines[l + 4].replace("If true: throw to monkey ", "")
        notDivisibleRecipient = lines[l + 5].replace("If false: throw to monkey ", "")
        monkey = Monkey(id, startingItems, operation, divisor, divisibleRecipient, notDivisibleRecipient, monkeyMap)
        monkeyMap[monkey.id] = monkey
        l += 7
    return monkeyMap

def calculateMonkeyBusiness(monkeys):
    return reduce(operator.mul, sorted(map(lambda m: m.inspectionCount, monkeys), reverse=True)[:2], 1)

def simulateRounds(monkeys, numRounds, reduceWorry):
    ceiling = reduce(operator.mul, map(lambda m: m.divisor, monkeys.values()))
    for monkey in monkeys.values():
        monkey.ceiling = ceiling

    for _ in range(1, numRounds + 1):
        for monkey in monkeys.values():
            monkey.inspectItems()
    
    for monkey in monkeys.values():
        print(f"Money {monkey.id} inspected items {monkey.inspectionCount} times")

        # print(f"After round {r}, the monkeys are holding items with these worry levels")
        # for monkey in monkeys.values():
        #     monkey.reportState()
    
    return calculateMonkeyBusiness(monkeys.values())

def solve(file):
    monkeys = process(file)
    print(f"Part 2: {simulateRounds(monkeys, 10000)}")

solve("inputs/11/full.txt")
