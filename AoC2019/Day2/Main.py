import os, sys
from time import time

from AoC2019.IntComp import IntComp

def Timer(func):
    def Timer_wrapper(*arg, rtrn:bool=True, prnt:bool=False, **args):
        """ rtrn: return the result if true
            prnt: print -- {the function that is being timed}: {result} -- {time it took}
            *arg and **args contain unnamed and named variables respectably to be passed to the function to be timed"""
        t0 = time()
        out = func(*arg, **args)
        if prnt == True:
            print( f"{str(func.__name__)}: {out}  -- {time()-t0}" )
        if rtrn:
            return out
    return Timer_wrapper

@ Timer
def parse(test:int, *arg, **args):
    r""" imports input file from "AoC2020\Day{day}\{f}"  """
    
    path = '\\'.join( os.path.abspath(__file__).split('\\')[:-1] )
    file_loc = f"""{path}\\{f"{f'test_{test}_' if test > 0 else ''}input.txt"}"""
    with open(file_loc) as f:
        comp = IntComp(f)
    return comp

@ Timer
def part1(comp, **args):
    """ inp = input; **args contains named arguments to be passed to the timer function mostly"""
    comp = comp.copy()
    print(comp.input_program == {i:each for i, each in enumerate(map(int, "1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,9,19,1,5,19,23,1,6,23,27,1,27,10,31,1,31,5,35,2,10,35,39,1,9,39,43,1,43,5,47,1,47,6,51,2,51,6,55,1,13,55,59,2,6,59,63,1,63,5,67,2,10,67,71,1,9,71,75,1,75,13,79,1,10,79,83,2,83,13,87,1,87,6,91,1,5,91,95,2,95,9,99,1,5,99,103,1,103,6,107,2,107,13,111,1,111,10,115,2,10,115,119,1,9,119,123,1,123,9,127,1,13,127,131,2,10,131,135,1,135,5,139,1,2,139,143,1,143,5,0,99,2,0,14,0".split(',')))} )
    comp.input_program[1] = 12
    comp.input_program[2] = 2
    process = comp.run()
    next(process)

    return comp.memory[0]

@ Timer
def part2(comp, goal=None, **args):
    """ inp = input; **args contains named arguments to be passed to the timer function mostly"""
    for noun in range(100):
        for verb in range(100):
            inst = comp.copy() # no writing is being done in any significant areas save .3 s
            inst.input_program[1] = noun
            inst.input_program[2] = verb
            process = inst.run()
            next(process)
            if inst.memory[0] == goal:
                return 100 * noun + verb

            


if __name__ == "__main__":
    """ files needed
        - input.txt
        - test_{x}_input.txt, with x the test number"""
    t0 = time()
    test = 0; prnt = test != 0
    inp = parse(test, prnt=prnt)
    part1(inp, prnt=True) # 3562672 == ans > 3562670
    part2(inp, goal = 19690720, prnt=True)
    print(f"Total time: {time()-t0}")