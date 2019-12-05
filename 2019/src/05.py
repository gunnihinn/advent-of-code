import argparse
import unittest


def partA(codes):
    cs = codes.copy()
    cs = run(cs)

def partB(codes):
    pass

def run(codes):
    p = 0
    while codes[p] != 99:
        if p == 180:
            #import pdb; pdb.set_trace()
            pass
        opcode = codes[p] % 100
        if opcode in {1, 2}:
            params = 3
        elif opcode in {3, 4}:
            params = 1
        else:
            raise Exception("Bad opcode {} in position {}".format(codes[p], p))

        modes = []
        m = codes[p] // 100
        for _ in range(params):
            modes.append(m % 10)
            m = m // 10
            assert 0 == m or m == 1, "Invalid mode {} in code {}".format(m, codes[p])

        args = []
        for i, mode in enumerate(modes[:-1]):
            val = codes[p + i + 1]
            if mode == 0:
                args.append(codes[val])
            elif mode == 1:
                args.append(val)

        if opcode == 4 and modes[0] == 0:
            args.append(codes[codes[p + params]])
        else:
            args.append(codes[p + params])

        if opcode == 1:
            codes[args[2]] = args[0] + args[1]
        elif opcode == 2:
            codes[args[2]] = args[0] * args[1]
        elif opcode == 3:
            codes[args[0]] = int(input("Input: "))
        elif opcode == 4:
            print(args[0])

        p += params + 1

    return codes


class TestProblem(unittest.TestCase):

    def test_run1(self):
        codes = [1, 0, 0, 0, 99]
        exp = [2, 0, 0, 0, 99]
        got = run(codes)
        self.assertEqual(got, exp)

    def test_run2(self):
        codes = [2, 3, 0, 3, 99]
        exp = [2, 3, 0, 6, 99]
        got = run(codes)
        self.assertEqual(got, exp)

    def test_run3(self):
        codes = [2, 4, 4, 5, 99, 0]
        exp = [2, 4, 4, 5, 99, 9801]
        got = run(codes)
        self.assertEqual(got, exp)

    def test_run4(self):
        codes = [1, 1, 1, 4, 99, 5, 6, 0, 99]
        exp = [30, 1, 1, 4, 2, 5, 6, 0, 99]
        got = run(codes)
        self.assertEqual(got, exp)

    def test_run5(self):
        codes = [1002, 4, 3, 4, 33, 99]
        exp = [1002, 4, 3, 4, 99, 99]
        got = run(codes)
        self.assertEqual(got, exp)

    def test_run6(self):
        codes = [1101, 100, -1, 4, 0, 99]
        exp = [1101, 100, -1, 4, 99, 99]
        got = run(codes)
        self.assertEqual(got, exp)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()

    with open(args.input) as fh:
        codes = [int(i) for i in fh.read().strip().split(',')]

    partA(codes)
    partB(codes)
