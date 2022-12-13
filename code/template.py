def parse(file):
    return [l.strip() for l in open(file).readlines()]

def solve(file):
    parsed = parse(file)
    print(parsed)
