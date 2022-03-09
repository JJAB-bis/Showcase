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
    pass

@ Timer
def part2(comp, goal=None, **args):
    """ inp = input; **args contains named arguments to be passed to the timer function mostly"""
    pass

            


if __name__ == "__main__":
    """ files needed
        - input.txt
        - test_{x}_input.txt, with x the test number"""
    t0 = time()
    test = 0; prnt = test != 0
    comp = parse(test, prnt=prnt)
    part1(comp, prnt=True)
    part2(comp, prnt=True)
    print(f"Total time: {time()-t0}")