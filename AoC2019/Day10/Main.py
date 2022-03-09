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
        lines = f.readlines()
    return lines

### supporting functions/classes- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -






import math

import numpy as np


class Station:
    def __init__(self, smap:str = None, chart = None):
        self.chart = self.read(smap)
        self.height, self.width = self.chart.shape
        self.ray_vectors = self.ray_pre_calc(sorted=True)
        self.asteroid_count = sum( sum(self.chart) )
    
    def sort_vectors(self, v,show:bool=False):
        v = list(sorted(v, key = lambda x: math.atan2(*x)))
        l = -1 + len(v)//4
        v = v[l:] + v[:l]
        if show: self.show_vectors(v)
        return v
    
    def show_vectors(self,v):
        i = 1; ox,oy = map(lambda x: x*2, self.chart.shape)
        zy,zx = map(lambda x: x*4, self.chart.shape)
        print(zy,zx)
        
        chart = np.zeros((zy,zx),dtype=int)
        chart[oy,ox] -= 1
        h,w = chart.shape
        
        for y,x in v:
            print(i,y,x)
            if all(((0 <= y+oy < h),(0 <= x+ox < w))):
                chart[y+oy,x+ox] += i
                i += 1
        print(chart)
        
        
    def scan(self):
        # print(self.chart)
        hits = np.zeros_like(self.chart,dtype=int)
        for y in range(self.height):
            for x in range(self.width):
                if self.chart[y,x] == 0:
                    continue
                hits[y,x] = self.ray_cast(y,x)
        #print(hits)
        pos = np.unravel_index( np.argmax(hits), hits.shape)
        print(pos,hits[pos])
        return pos,hits[pos]
                
    def ray_pre_calc(self, sorted=False):
        rays = set()
        for y in range(self.height):
            for x in range(self.width):
                if y ==0 and x==0:
                    continue
                # print(x,y)
                gcd = math.gcd(y,x)
                # print(gcd)
                # rays.add( (y//gcd,x//gcd) )
                dy,dx = (y//gcd,x//gcd)
                rays |= { (dy,dx),(-dy,dx),(dy,-dx),(-dy,-dx) }
        return self.sort_vectors(rays) if sorted else rays
        
    def ray_pre_calc_quad(self):
        rays = set()
        for y in range(self.height):
            for x in range(self.width):
                if y ==0 and x==0:
                    continue
                # print(x,y)
                gcd = math.gcd(y,x)
                # print(gcd)
                rays.add( (y//gcd,x//gcd) )
                #rays.append( (y//gcd,x//gcd) )
        return rays
        
    def ray_cast(self,Y,X):
        count = 0
        for dy,dx in self.ray_vectors:
            y,x = Y+dy,X+dx
            while all(((0 <= y < self.height),(0 <= x < self.width))):
                if self.chart[y,x] > 0:
                    count += 1
                    break
                y+=dy
                x+=dx
        return count
        
                
    def read(self,smap:str, out:str='bin') -> 'np.bin_arr | np.str_arr':
        m = np.array([list(each) for each in smap.split()])
        if out == 'bin':
            n = np.zeros_like(m,dtype=int)
            n[m == '#'] = 1
            return n
        return m
        
    def vaporize(self,Y,X):
        tally = np.zeros_like(self.chart)
        chart = self.chart.copy()
        chart[Y,X] = 0
        tally[Y,X] = -1
        count = 0
        
        i = 0
        while sum(sum(chart)) > 0:
            for dy,dx in self.ray_vectors:
                y,x = Y+dy,X+dx
                while all(((0 <= y < self.height),(0 <= x < self.width))):
                    if chart[y,x] > 0:
                        count += 1
                        chart[y,x] = 0
                        tally[y,x] = count
                        if False and (count+1)%9==0:
                            print(tally)
                            print()
                        break
                    y+=dy
                    x+=dx
        return np.where(tally==200)













### - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

@ Timer
def part1(inp, **args):
    """ inp = input; **args contains named arguments to be passed to the timer function mostly"""
    test = Station( inp[0] )
    return test.scan()

@ Timer
def part2(inp,pos, **args):
    """ inp = input; **args contains named arguments to be passed to the timer function mostly"""
    y,x = pos
    test = Station( inp[0] )
    y,x = test.vaporize(y,x)
    out = x*100+y
    return out[0]


if __name__ == "__main__":
    """ files needed
        - input.txt
        - test_{x}_input.txt, with x the test number"""
    t0 = time()
    test = 0; prnt = test != 0
    inp = parse(test, prnt=prnt)
    pos,ans = part1(inp, prnt=True)
    part2(inp, pos, prnt=True)
    print(f"Total time: {time()-t0}")