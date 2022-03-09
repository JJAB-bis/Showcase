import os, sys
from time import time

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
        lines = list(map(int, [each.strip() for each in f.readlines()]))
    return lines

@ Timer
def part1(inp, **args):
    """ inp = input; **args contains named arguments to be passed to the timer function mostly"""
    def fuel_calc(mass):
        return mass//3 - 2
    return sum(list(map(fuel_calc, inp)))

@ Timer
def part2(inp, **args):
    """ inp = input; **args contains named arguments to be passed to the timer function mostly"""
    def fuel_calc_improved(mass):
        t = 0
        while mass > 0:
            mass = mass//3 - 2
            mass = mass * int(mass > 0)
            t += mass
        return t
    return sum(list(map(fuel_calc_improved, inp)))

if __name__ == "__main__":
    """ files needed
        - input.txt
        - test_{x}_input.txt, with x the test number"""
    t0 = time()
    day = 0; test = 0; prnt = test != 0
    inp = parse(day,test, prnt=prnt)
    part1(inp, prnt=True)
    part2(inp, prnt=True)
    print(f"Total time: {time()-t0}")