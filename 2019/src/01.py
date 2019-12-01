import argparse
import unittest


def partA(lines):
    return sum(fuel(m) for m in lines)

def partB(lines):
    return sum(total_fuel(m) for m in lines)

def fuel(mass: int) -> int:
    return mass // 3 - 2

def total_fuel(mass: int) -> int:
    total = 0
    while True:
        mass = fuel(mass)
        if mass >= 0:
            total += mass
        else:
            break

    return total
        

class TestProblem(unittest.TestCase):

    def test_fuel(self):
        self.assertEqual(fuel(12), 2)
        self.assertEqual(fuel(14), 2)
        self.assertEqual(fuel(1969), 654)
        self.assertEqual(fuel(100756), 33583)

    def test_total(self):
        self.assertEqual(total_fuel(14), 2)
        self.assertEqual(total_fuel(1969), 966)
        self.assertEqual(total_fuel(100756), 50346)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()

    with open(args.input) as fh:
        lines = [int(l) for l in fh]

    print(partA(lines))
    print(partB(lines))
