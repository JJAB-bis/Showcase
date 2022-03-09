import os, sys
import re

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
        lines = [int(each) for each in f.read().strip().split('-')]
    return lines

@ Timer
def part1(inp, **args):
    """ inp = input; **args contains named arguments to be passed to the timer function mostly"""
    def validate(password, lower,upper):
        s_pass = str(password)
        if len(s_pass) != 6:
            return False
        elif lower > password > upper:
            return False
        elif ''.join(sorted(s_pass)) != s_pass:
            return False
        for i, n in enumerate(s_pass[1:]):
            if s_pass[i] == n:
                return True
        return False
    lower, upper = inp[0],inp[1]+1
    count = 0
    for password in range(lower,upper):
        if validate(password, lower, upper):
            count += 1
    return count

@ Timer
def part2(inp, **args):
    """ inp = input; **args contains named arguments to be passed to the timer function mostly"""
    pat = re.compile(''.join([f"({i}*)" for i in range(10)]))
    def validate(password, lower,upper):
        s_pass = str(password)
        grouped = [len(each) for each in re.search(pat, s_pass).groups() ]
        if sum(grouped) != 6:
            return False
        elif lower > password > upper:
            return False
        elif ''.join(sorted(s_pass)) != s_pass:
            return False

        return any([each == 2 for each in grouped])

    lower, upper = inp[0],inp[1]+1
    count = 0
    for password in range(lower,upper):
        if validate(password, lower, upper):
            count += 1
    return count

if __name__ == "__main__":
    """ files needed
        - input.txt
        - test_{x}_input.txt, with x the test number"""
    t0 = time()
    test = 0; prnt = test != 0
    inp = parse(test, prnt=prnt)
    part1(inp, prnt=True)
    part2(inp, prnt=True) # ans > 134
    print(f"Total time: {time()-t0}")