import argparse
import hashlib
import unittest


def partA(seed, target=5):
    start = '0' * target
    seed = seed.encode('utf-8')

    n = 1
    while True:
        m = hashlib.md5()
        m.update(seed)
        m.update('{}'.format(n).encode('utf-8'))
        h = m.hexdigest()
        if h.startswith(start):
            return n
        n += 1

def partB(seed, target):
    return partA(seed, target)


class TestProblem(unittest.TestCase):

    def test_mine(self):
        self.assertEqual(partA('abcdef'), 609043)
        self.assertEqual(partA('pqrstuv'), 1048970)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()

    with open(args.input) as fh:
        seed = fh.read().strip()

    print(partA(seed))
    print(partB(seed, target=6))
