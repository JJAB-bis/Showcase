import unittest
import os
from IntComp import IntComp

class Debugging_Manager:
    def __init__(self, step=False):
        self.step = step

class TestIntComp(unittest.TestCase):
    def setUp(self):
        self.path = '\\'.join( os.path.abspath(__file__).split('\\')[:-1] ) + '\\Day'

    def test_Day2(self, debugging = False):
        path = f"{self.path}{2}"
        expected = [
            [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50],
            [2,0,0,0,99],
            [2,3,0,6,99],
            [2,4,4,5,99,9801],
            [30,1,1,4,2,5,6,0,99]
        ]
        expected = [ 
            {i:each for i,each in enumerate(EACH) } for EACH in expected
        ]
        for i, res in enumerate(expected):
            t = f"{path}\\test_{i+1}_input.txt"
            with open(t) as f:
                comp = IntComp(f)
            process = comp.run()
            next(process)
            if debugging: print(i, comp.input_program, res)
            self.assertEqual(comp.memory, res)
        t = f"{path}\\input.txt"
        res = 3562672
        with open(t) as f:
            comp = IntComp(f)
        comp.input_program[1] = 12
        comp.input_program[2] = 2
        # mem[1] = 12
        # mem[2] = 2
        process = comp.run()
        next(process)
        if debugging: print(i+1, comp.memory[0], res)
        self.assertEqual(comp.memory[0], res)
        breaking = False; goal = 19690720
        for noun in range(100):
            if breaking:
                break
            noun = 82
            for verb in range(100):
                i += 1
                verb = 50
                comp.input_program[1] = noun
                comp.input_program[2] = verb
                process = comp.run()
                next(process)
                if comp.memory[0] == goal:
                    if debugging: print(f"mem = {comp.memory[0]} - {goal = } /-\\ {noun=} + {verb=} == {8250}")
                    self.assertEqual(100 * noun + verb, 8250)
                    breaking = True
                    break

    def test_Day5(self, debugging = True):
        pass

    def test_Day9(self, debugging = True):
        path = f"{self.path}{9}"
        expected = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]

        i = 2
        t = f"{path}\\test_{i}_input.txt"
        with open(t) as f:
            comp = IntComp(f)
        process = comp.run()
        next(process)
        self.assertEqual(comp.output, [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99])

        i = 3
        t = f"{path}\\test_{i}_input.txt"
        with open(t) as f:
            comp = IntComp(f)
        process = comp.run()
        next(process)
        self.assertEqual(len(str(comp.output[0])), len(str(1219070632396864)))

        i = 4
        t = f"{path}\\test_{i}_input.txt"
        with open(t) as f:
            comp = IntComp(f)
        process = comp.run()
        next(process)
        self.assertEqual(comp.output, [1125899906842624])


    def test_Code3(self, debugging = False):
        path = f"{self.path}{5}"
        t = f"{path}\\test_{1}_input.txt"
        with open(t) as f:
            comp = IntComp(f)
        process = comp.run()
        next(process)
        self.assertEqual(comp.memory, {i:each for i,each in enumerate([1002, 4, 3, 4, 99])})

    def test_Code4(self, msg=42069, debugging = False):
        path = f"{self.path}{5}"
        t = f"{path}\\test_{2}_input.txt"
        with open(t) as f:
            comp = IntComp(f)
        process = comp.run()
        next(process)
        process.send(msg)
        self.assertEqual(comp.output, [msg])
    
    def test_Code8_pos(self, day=5,test=3, debugging = False):
        t = f"{self.path}{day}\\test_{test}_input.txt"
        with open(t) as f:
            comp = IntComp(f)
        expected = (0,1,0) 
        for i,msg in enumerate(range(7,10)):
            process = comp.run()
            next(process)
            process.send(msg)
            self.assertEqual(comp.output, [expected[i]])
    
    def test_Code8_imm(self, day=5,test=5, debugging = False):
        t = f"{self.path}{day}\\test_{test}_input.txt"
        with open(t) as f:
            comp = IntComp(f)
        expected = (0,1,0) 
        for i,msg in enumerate(range(7,10)):
            process = comp.run()
            next(process)
            process.send(msg)
            self.assertEqual(comp.output, [expected[i]])
    
    
    def test_Code7_pos(self, day=5,test=4, debugging = False):
        t = f"{self.path}{day}\\test_{test}_input.txt"
        with open(t) as f:
            comp = IntComp(f)
        expected = (1,0,0) 
        for i,msg in enumerate(range(7,10)):
            process = comp.run()
            next(process)
            process.send(msg)
            self.assertEqual(comp.output, [expected[i]])
    
    def test_Code7_imm(self, day=5,test=6, debugging = False):
        t = f"{self.path}{day}\\test_{test}_input.txt"
        with open(t) as f:
            comp = IntComp(f)
        expected = (1,0,0) 
        for i,msg in enumerate(range(7,10)):
            process = comp.run()
            next(process)
            process.send(msg)
            self.assertEqual(comp.output, [expected[i]])
    
    def test_Code_5_6_pos(self, day=5, test=7, debugging = False):
        t = f"{self.path}{day}\\test_{test}_input.txt"
        with open(t) as f:
            comp = IntComp(f)
        expected = (0, 1) 
        for i,msg in enumerate([0,5]):
            process = comp.run()
            next(process)
            process.send(msg)
            self.assertEqual(comp.output, [expected[i]])

    
    def test_Code_5_6_imm(self, day=5, test=8, debugging = False):
        t = f"{self.path}{day}\\test_{test}_input.txt"
        with open(t) as f:
            comp = IntComp(f)
        expected = (0, 1) 
        for i,msg in enumerate([0,5]):
            process = comp.run()
            next(process)
            process.send(msg)
            self.assertEqual(comp.output, [expected[i]])

    
    def test_Code_5_to_8(self, day=5, test=9, debugging = False):
        t = f"{self.path}{day}\\test_{test}_input.txt"
        with open(t) as f:
            comp = IntComp(f)
        expected = (999,1000,1001) 
        for i,msg in enumerate([5,8,10]):
            process = comp.run()
            next(process)
            process.send(msg)
            self.assertEqual(comp.output, [expected[i]])

    def test_Code_9(self, day=9, debugging = False):
        t = f"{self.path}{day}\\test_{1}_input.txt"
        with open(t) as f:
            comp = IntComp(f)
        expected = 66
        relative_base = 2000
        comp.input_program[1985] = expected
        process = comp.run(relative_base=relative_base)
        next(process)
        
        self.assertEqual(comp.output, [expected])


if __name__ == '__main__':
    unittest.main()