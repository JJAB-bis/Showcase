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
    
    pattern = re.compile('x=([-+\d]+),.*y=([-+\d]+),.*z=([-+\d]+)\D')

    path = '\\'.join( os.path.abspath(__file__).split('\\')[:-1] )
    file_loc = f"""{path}\\{f"{f'test_{test}_' if test > 0 else ''}input.txt"}"""
    with open(file_loc) as f:
        lines = [list(map(int,re.search(pattern, each).groups())) for each in f.readlines()]

    l = len(lines)

    array = np.zeros((l,6), dtype = int)
    for i in range(l):
        array[i,:3] = lines[i]

    return array

### supporting functions/classes- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

import numpy as np
import math

class System:

    class Planet:
        def __init__(self, system, vector):
            self.system = system
            self.vector = vector
            self.start  = vector.copy()
            self.pos    = self.vector[:3]
            self.vel    = self.vector[3:]

            print('Planet: ', self.pos, self.vel)

        def __str__(self):
            return str(self.pos)
                    
        def calc_energy(self):
            return sum(abs(self.pos)) * sum(abs(self.vel))

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def __init__(self, planets):
        self.steps   = 0
        self.array   = planets.copy()
        self.start   = planets.copy()
        self.cycled  = np.zeros(planets.shape[0], dtype = int)
        self.cycled_step = np.zeros(planets.shape[0], dtype = int)
        self.planets = [self.Planet(self, vector) for vector in self.array]

    def update(self):
        # calc_dv()
        h,w = self.array.shape
        for i in range(h):
            r = np.r_[0:i, i+1:h]
            #               adds the amount of planets with smaller x|y|z,     substracts      the planets with larger x|y|z from planet i's velocity
            self.array[i,3:] += np.sum(self.array[i,:3] < self.array[r,:3], axis=0) - np.sum(self.array[i,:3] > self.array[r,:3], axis=0)
        # apply dv
        self.array[:,:3] = self.array[:,:3] + self.array[:,3:]
        # increase step counter        
        self.steps += 1

    def calc_energy(self):
        total = 0
        for each in self.planets:
            total += each.calc_energy()
        return total

    def update_cycled(self, n= [1]):
        if self.steps == 0:
            return True
            
        s = ( np.sum((self.start - self.array != 0),axis = 1 ) == 0 )

        self.cycled[self.cycled == 0] = s[self.cycled == 0] * self.steps
        if (self.cycled != 0).any() and (s != 0).any():
            print(self.steps, self.cycled)
            # """
            print(f'---------------{self.steps = }----------------------')
            print(self.start)
            print()
            print(self.array)
            print()
            print(self.start - self.array)
            print()
            print(self.start - self.array == 0)
            print()
            print( np.sum((self.start - self.array != 0),axis = 1 ) == 0 )
            print('----------------------------------------')
            # """
            input('\n')
        return (self.cycled == 0).any()













### - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -



@ Timer
def part1(inp, test=0, **args):
    """ inp = input; **args contains named arguments to be passed to the timer function mostly"""
    
    r = [1000,10,100][test]

    system = System(inp)
    for _ in range(r):
        system.update()
    print(system.steps)
    print(system.array)
    return system.calc_energy()

@ Timer
def part2(inp, **args):
    """ inp = input; **args contains named arguments to be passed to the timer function mostly"""
    system = System(inp)
    print(system.array)
    i = 0
    print('running ...  ', end='', flush=True)
    while system.update_cycled():
        system.update()
        # print('-', system.cycled)
    print(system.array)
    print(f"{system.steps=}")
    print(f"{system.cycled=}")
    print('-', math.lcm(*list(system.cycled)),   4686774924)
    print('-', math.lcm(*list(system.cycled)) == 4686774924)
    
    


if __name__ == "__main__":
    """ files needed
        - input.txt
        - test_{x}_input.txt, with x the test number"""
    t0 = time()
    test = 0; prnt = test != 0
    inp = parse(test, prnt=prnt)
    part1(inp.copy(), test, prnt=True) # 12082 == ans > 1316(100 steps ipv 1000)
    part2(inp.copy(), prnt=True)
    print(f"Total time: {time()-t0}")