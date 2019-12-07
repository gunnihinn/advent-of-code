import argparse
import unittest

from vm import VM

def partA(codes):
    vm = VM(codes, [1])
    vm.run()
    print(vm.output)

def partB(codes):
    vm = VM(codes, [5])
    vm.run()
    print(vm.output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()

    with open(args.input) as fh:
        codes = [int(i) for i in fh.read().strip().split(',')]

    partA(codes)
    partB(codes)
