class Directory:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.children = {}
        self.size = 0

    def addChild(self, child):
        if child in self.children:
            return
        self.children[child.name] = child
        self.adjustSize(child.size)

    def adjustSize(self, inc):
        self.size += inc
        if self.parent:
            self.parent.adjustSize(inc)

class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size

def process(file):
    lines = [l.strip() for l in open(file).readlines()]
    return lines

def parseObject(line, parent):
    splt = line.split(" ")
    if splt[0] == "dir":
        return Directory(splt[1], parent)
    else:
        return File(splt[1], int(splt[0]))

def buildFileSystem(lines):
    root = Directory("", None)
    currDirectory = root

    for line in lines:
        if line.startswith("$ cd"):
            destination = line[5:]
            if destination == "/":
                currDirectory = root
            elif destination == "..":
                currDirectory = currDirectory.parent
            else:
                currDirectory = currDirectory.children[destination]
        elif not line.startswith("$"):
            currDirectory.addChild(parseObject(line, currDirectory))

    return root

def getDirectories(root):
    directories = []
    next = [root]
    while len(next):
        curr = next.pop()
        directories.append(curr)
        for child in curr.children.values():
            if isinstance(child, Directory):
                next.append(child)
    return directories

def getDirectorySizes(root):
    return list(map(lambda d : d.size, getDirectories(root)))

def solvePart1(root):
    return sum(filter(lambda s: s <= 100000, getDirectorySizes(root)))

def solvePart2(root):
    currentUnusedSpace = 70000000 - root.size
    needToDelete = 30000000 - currentUnusedSpace
    return min(filter(lambda s: s >= needToDelete, getDirectorySizes(root)))

def solve(file):
    fileSystem = buildFileSystem(process(file))
    print(f"Part 1: {solvePart1(fileSystem)}")
    print(f"Part 2: {solvePart2(fileSystem)}")

solve("inputs/07/full.txt")
