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
        lines = [each.strip().split(',') for each in f.readlines()]
    return lines


class Board:
    dirs = {
        'R' : (1 , 0),
        'D' : (0 ,-1),
        'L' : (-1, 0),
        'U' : (0 , 1),
    }
    def __init__(self, instructions):
        self.isntructions = instructions
        self.wires = {i:self.lay_wires(each) for i,each in enumerate(instructions) }

    def part_1(self):
        it = iter(self.wires.values())
        crossing = set(next(it).keys())
        for each in it:
            each = set(each.keys())
            crossing &= each
        return crossing
    
    def part_2(self):
        crossings = self.part_1()
        out = float('inf'); closest = None
        for cross in crossings:
            s = 0 
            for wire in self.wires.values():
                s += wire[cross]
            if s < out:
                closest = cross
                out = s
        return out


    def lay_wires(self, wire):
        out = {}
        x,y = 0,0
        l = 0
        for each in wire:
            d,n = each[0], int(each[1:])
            # print(d,n)
            dx,dy = self.dirs[d]
            for i in range(n):
                l += 1
                x,y = x+dx,y+dy
                out[(x,y)] = l
        return out






@ Timer
def part1(inp, **args):
    """ inp = input; **args contains named arguments to be passed to the timer function mostly"""
    b = Board(inp)
    crossing = b.part_1()
    crossing = [[abs(each) for each in point] for point in crossing]
    return min(list(map(lambda a : sum(a), crossing)))

@ Timer
def part2(inp, **args):
    """ inp = input; **args contains named arguments to be passed to the timer function mostly"""
    b = Board(inp)
    return b.part_2()

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