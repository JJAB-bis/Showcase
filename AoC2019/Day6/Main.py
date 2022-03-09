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
        lines = [each.strip() for each in f.readlines()]
    return lines

### supporting functions/classes- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class System:
    def __init__(self, inp):
        self.planets = self.build(inp)
        self.planets['COM'].set_depth()

    def build(self,inp):
        out = {}
        for each in inp:
            parent,child = each.split(')')
            try:
                parent = out[parent]
            except:
                parent = Planet(parent)
                out[parent.name] = parent
            try:
                child  = out[child]
            except:
                child  = Planet(child)
                out[child.name] = child
            parent.children.append(child)
            child.parent = parent
        return out
    
    def checksum(self):
        s = 0
        for p in self.planets.values():
            s += p.depth
        return s

    def __repr__(self):
        return str(self.planets)

class Ship:
    def __init__(self, start = None, goal = None):
        self.current = start
        self.goal    = goal
        self.steps   = 0
    
    def crawl_up(self):
        while self.goal not in self.current.sub_orbits:
            self.current = self.current.parent
            self.steps += 1

    def crawl_down(self):
        while self.goal not in self.current.children:
            for each in self.current.children:
                if self.goal in each.sub_orbits:
                    break
            self.current = each
            self.steps += 1


class Planet:
    def __init__(self, name, parent=None, children = None):
        self.name     = name
        self.parent   = parent
        self.children = [] if children is None else children
        self.depth    = 0
        
    def set_depth(self):
        self.depth = 0 if self.parent is None else self.parent.depth + 1 
        for each in self.children:
            each.set_depth()

    @property
    def sub_orbits(self):
        out = set(self.children)
        for each in self.children:
            out |= each.sub_orbits
        return out

    def __repr__(self):
        return self.name










### - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

@ Timer
def part1(inp, **args):
    """ inp = input; **args contains named arguments to be passed to the timer function mostly"""
    system = System(inp)
    return system.checksum()

@ Timer
def part2(inp, **args):
    """ inp = input; **args contains named arguments to be passed to the timer function mostly"""
    system = System(inp)
    ship = Ship(system.planets['YOU'].parent, system.planets['SAN'])
    ship.crawl_up()
    ship.crawl_down()
    return ship.steps



if __name__ == "__main__":
    """ files needed
        - input.txt
        - test_{x}_input.txt, with x the test number"""
    t0 = time()
    test = 0; prnt = test != 0
    inp = parse(test, prnt=prnt)
    part1(inp, prnt=True)
    part2(inp, prnt=True)
    print(f"Total time: {time()-t0}")