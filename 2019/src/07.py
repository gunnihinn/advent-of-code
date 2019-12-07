import argparse
import itertools
import unittest

input_1 = None
input_2 = None
output = 0

def partA(codes):
    global input_1
    global input_2
    global output

    signals = []
    for phase in itertools.permutations(range(5), 5):
        input_2 = 0
        for p in phase:
            input_1 = p
            cs = codes.copy()
            cs = run(cs)
            input_2 = output
        signals.append(output)

    return max(signals)

def partB(codes):
    pass

def run(codes):
    global input_1
    global input_2
    global output

    input_count = 0
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
            if input_count == 0:
                codes[p_out] = input_1
                input_count += 1
            elif input_count == 1:
                codes[p_out] = input_2
                input_count += 1
            else:
                raise Exception("Too much input")
        elif opcode == 4:
            output = args[0]
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
