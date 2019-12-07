import argparse
import itertools
import unittest

from src.vm import VM

def partA(codes):
    signals = []
    for phase in itertools.permutations(range(5), 5):
        input_2 = 0
        out = None
        for p in phase:
            vm = VM(codes, [p, input_2])
            vm.run()
            input_2 = vm.output
            out = vm.output
        signals.append(out)

    return max(signals)

def partB(codes):
    pass


class TestProblem(unittest.TestCase):

    def test_run1(self):
        codes = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
        exp = 43210
        got = partA(codes)
        self.assertEqual(got, exp)

    def test_run2(self):
        codes = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
        exp = 54321
        got = partA(codes)
        self.assertEqual(got, exp)

    def test_run3(self):
        codes = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
        exp = 65210
        got = partA(codes)
        self.assertEqual(got, exp)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()

    with open(args.input) as fh:
        codes = [int(i) for i in fh.read().strip().split(',')]

    print(partA(codes))
    print(partB(codes))
