def process(file):
    return [l.strip() for l in open(file).readlines()]

def solve(file):
    processed = process(file)
    print(processed)
