import os, sys
from time import time
import re
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
    
    pattern = re.compile('([\d]+)\s(\w+)')
    path = '\\'.join( os.path.abspath(__file__).split('\\')[:-1] )
    file_loc = f"""{path}\\{f"{f'test_{test}_' if test > 0 else ''}input.txt"}"""
    with open(file_loc) as f:
        lines = [ re.findall(pattern, line) for line in f.readlines()]
    return lines

### supporting functions/classes- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class Formula:
    def __init__(self,raw_form):
        self.out = { i:int(n) for n,i in [raw_form[-1]] }
        self.inp = { i:int(n) for n,i in raw_form[:-1]  }
        self.name = list(self.out.keys())[0]

        print ( self.name, self.inp, self.out )
    def __repr__(self):

        return f"Form-{self.name}"
    def __str__(self):
        s = f"{self.name} {self.out[self.name]} <= "

        for key,value in self.inp.items():
            s += f"{key} {value}, "

        return s[:-2]

class LookUp:
    def __init__(self, inp):
        print(inp)
        self.formulas = [ Formula(each) for each in inp ]
        self.formulas = { form.name: form for form in self.formulas}
        print(self.formulas)
    
    def calc_min_ore(self, fuel = 1):
        required = {'FUEL': fuel}
        total_ore = 0
        break_i = 0

        while required and break_i<5:
            key,value = required.popitem()
            print(key, value)
            print(self.formulas[key])
            try:
                for form_key,form_value in self.formulas[key].out.items():
                    try:
                        required[form_key] += value*form_value
                    except:
                        required[form_key] = value*form_value
            except KeyError:
                total_ore += value

            break_i += 1



















### - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

@ Timer
def part1(inp,test, **args):
    """ inp = input; **args contains named arguments to be passed to the timer function mostly"""
    test_restults = [0,31,165,13312,180697,2210736][test]

    tree = LookUp(inp)
    tree.calc_min_ore(2)

@ Timer
def part2(inp, **args):
    """ inp = input; **args contains named arguments to be passed to the timer function mostly"""
    pass

if __name__ == "__main__":
    """ files needed
        - input.txt
        - test_{x}_input.txt, with x the test number"""
    t0 = time()
    test = 1; prnt = test != 0
    inp = parse(test, prnt=prnt)
    part1(inp,test, prnt=True)
    # part2(inp, prnt=True)
    print(f"Total time: {time()-t0}")