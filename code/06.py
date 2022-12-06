from collections import deque

def process(file):
    lines = [l.strip() for l in open(file).readlines()]
    return lines[0]
 
def findMarker(str, size):
    buffer = deque()
    for i, c in enumerate(str):
        if len(buffer) == size:
            buffer.popleft()
        buffer.append(c)
        if len(set(buffer)) == size:
            return i + 1

def solve(file):
    processed = process(file)
    print(f"Part 1: {findMarker(processed, 4)}")
    print(f"Part 2: {findMarker(processed, 14)}")

solve("inputs/06/full.txt")
