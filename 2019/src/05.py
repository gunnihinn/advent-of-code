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
        opcode = codes[p] % 100
        if opcode in {1, 2, 7, 8}:
            n_in = 2
            n_out = 1
        elif opcode == 3:
            n_in = 0
            n_out = 1
        elif opcode == 4:
            n_in = 1
            n_out = 0
        elif opcode in {5, 6}:
            n_in = 2
            n_out = 0
        else:
            raise Exception("Bad opcode {} in position {}".format(codes[p], p))

        args = []
        mode = codes[p] // 100
        for i in range(n_in):
            val = codes[p + i + 1]
            if mode % 10 == 0:
                args.append(codes[val])
            elif mode % 10 == 1:
                args.append(val)
            else:
                raise Exception("Invalid mode {} in code {}".format(m, codes[p]))
            mode = mode // 10

        if n_out:
            p_out = codes[p + n_in + 1]
        else:
            p_out = None

        if opcode == 1:
            codes[p_out] = args[0] + args[1]
        elif opcode == 2:
            codes[p_out] = args[0] * args[1]
        elif opcode == 3:
            codes[p_out] = int(input("Input: "))
        elif opcode == 4:
            print(args[0])
        elif opcode == 5:
            if args[0] != 0:
                p = args[1]
                continue
        elif opcode == 6:
            if args[0] == 0:
                p = args[1]
                continue
        elif opcode == 7:
            if args[0] < args[1]:
                codes[p_out] = 1
            else:
                codes[p_out] = 0
        elif opcode == 8:
            if args[0] == args[1]:
                codes[p_out] = 1
            else:
                codes[p_out] = 0

        p += n_in + n_out + 1

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
