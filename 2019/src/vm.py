import unittest

class VM:

    def __init__(self, codes, inputs=None):
        self.p = 0
        if inputs is not None:
            self.inputs = [int(i) for i in inputs]
            self.inputs.reverse()
        self.output = None
        self.codes = codes.copy()

    def run(self):
        while self.codes[self.p] != 99:
            opcode = self.codes[self.p] % 100
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
                raise Exception("Bad opcode {} in position {}".format(self.codes[self.p], self.p))

            args = []
            mode = self.codes[self.p] // 100
            for i in range(n_in):
                val = self.codes[self.p + i + 1]
                if mode % 10 == 0:
                    args.append(self.codes[val])
                elif mode % 10 == 1:
                    args.append(val)
                else:
                    raise Exception("Invalid mode {} in code {}".format(m, self.codes[self.p]))
                mode = mode // 10

            if n_out:
                p_out = self.codes[self.p + n_in + 1]
            else:
                p_out = None

            if opcode == 1:
                self.codes[p_out] = args[0] + args[1]
            elif opcode == 2:
                self.codes[p_out] = args[0] * args[1]
            elif opcode == 3:
                self.codes[p_out] = self.inputs.pop()
            elif opcode == 4:
                self.output = args[0]
            elif opcode == 5:
                if args[0] != 0:
                    self.p = args[1]
                    continue
            elif opcode == 6:
                if args[0] == 0:
                    self.p = args[1]
                    continue
            elif opcode == 7:
                if args[0] < args[1]:
                    self.codes[p_out] = 1
                else:
                    self.codes[p_out] = 0
            elif opcode == 8:
                if args[0] == args[1]:
                    self.codes[p_out] = 1
                else:
                    self.codes[p_out] = 0

            self.p += n_in + n_out + 1


class TestProblem(unittest.TestCase):

    def test_run1(self):
        codes = [1, 0, 0, 0, 99]
        exp = [2, 0, 0, 0, 99]
        vm = VM(codes)
        vm.run()
        got = vm.codes
        self.assertEqual(got, exp)

    def test_run2(self):
        codes = [2, 3, 0, 3, 99]
        exp = [2, 3, 0, 6, 99]
        vm = VM(codes)
        vm.run()
        got = vm.codes
        self.assertEqual(got, exp)

    def test_run3(self):
        codes = [2, 4, 4, 5, 99, 0]
        exp = [2, 4, 4, 5, 99, 9801]
        vm = VM(codes)
        vm.run()
        got = vm.codes
        self.assertEqual(got, exp)

    def test_run4(self):
        codes = [1, 1, 1, 4, 99, 5, 6, 0, 99]
        exp = [30, 1, 1, 4, 2, 5, 6, 0, 99]
        vm = VM(codes)
        vm.run()
        got = vm.codes
        self.assertEqual(got, exp)

    def test_run5(self):
        codes = [1002, 4, 3, 4, 33, 99]
        exp = [1002, 4, 3, 4, 99, 99]
        vm = VM(codes)
        vm.run()
        got = vm.codes
        self.assertEqual(got, exp)

    def test_run6(self):
        codes = [1101, 100, -1, 4, 0, 99]
        exp = [1101, 100, -1, 4, 99, 99]
        vm = VM(codes)
        vm.run()
        got = vm.codes
        self.assertEqual(got, exp)
