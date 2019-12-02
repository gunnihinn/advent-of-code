import argparse
import unittest


def partA(codes):
    cs = codes.copy()
    cs[1] = 12
    cs[2] = 2
    cs = run(cs)

    return cs[0]

def partB(codes):
    for i in range(0, 100):
        for j in range(0, 100):
            cs = codes.copy()
            cs[1] = i
            cs[2] = j
            try:
                cs = run(cs)
            except Exception as e:
                raise Exception("Error in input ({}, {})".format(i, j)) from e

            if cs[0] == 19690720:
                return 100 * i + j

    raise Exception("Terminated without an answer")


def run(codes):
    p = 0
    while codes[p] != 99:
        p_op1 = codes[p+1]
        p_op2 = codes[p+2]
        p_res = codes[p+3]
        if codes[p] == 1:
            codes[p_res] = codes[p_op1] + codes[p_op2]
        elif codes[p] == 2:
            codes[p_res] = codes[p_op1] * codes[p_op2]
        else:
            raise Exception("Bad opcode {} in position {}".format(codes[p], p))
        p += 4

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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()

    with open(args.input) as fh:
        codes = [int(i) for i in fh.read().strip().split(',')]

    print(partA(codes))
    print(partB(codes))
