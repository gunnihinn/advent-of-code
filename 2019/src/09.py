import argparse
import itertools
import unittest

from src.vm import VM

def partA(codes):
    vm = VM(codes, [1])
    vm.run()
    return vm.output

def partB(codes):
    vm = VM(codes, [2])
    vm.run()
    return vm.output


class TestProblem(unittest.TestCase):

    def test_run0(self):
        codes = [109, 19, 204, -34, 99]
        vm = VM(codes)
        vm.rp = 2000
        vm._codes[1985] = 1
        vm.run()
        exp = 1
        got = vm.output
        assert got == exp

    def test_run1(self):
        codes = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
        vm = VM(codes)
        vm.run()
        exp = codes
        got = vm._output
        assert got == exp

    def test_run2(self):
        codes = [1102,34915192,34915192,7,4,7,99,0]
        vm = VM(codes)
        vm.run()
        got = "{}".format(vm.output)
        assert len(got) == 16

    def test_run3(self):
        codes = [104,1125899906842624,99]
        vm = VM(codes)
        vm.run()
        exp = 1125899906842624
        got = vm.output
        assert got == exp



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()

    with open(args.input) as fh:
        codes = [int(i) for i in fh.read().strip().split(',')]

    print(partA(codes))
    print(partB(codes))
