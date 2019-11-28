import argparse

def partA(blob):
    c = 0
    for char in blob:
        if char == '(':
            c += 1
        elif char == ')':
            c -= 1
        else:
            raise Exception("Unknown char '{}'".format(char))

    return c

def partB(blob):
    c = 0
    for i, char in enumerate(blob):
        if char == '(':
            c += 1
        elif char == ')':
            c -= 1
        else:
            raise Exception("Unknown char '{}'".format(char))

        if c == -1:
            return i + 1

    raise Exception("Never entered basement")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()

    with open(args.input) as fh:
        blob = fh.read().strip()
        print(partA(blob))
        print(partB(blob))
