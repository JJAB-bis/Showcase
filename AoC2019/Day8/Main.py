import os, sys
import numpy as np
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
        lines = np.array([int(each) for each in f.read()])
    return lines

### supporting functions/classes- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def np_2_str(arr):
    arr = arr.tolist()
    s = '\n'
    for row in arr:
        for sq in row:
            s += "#" if sq else ' '
        s += '\n'
    print(s)


### - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

@ Timer
def part1(inp, dims, debugging=False, **args):
    """ inp = input; **args contains named arguments to be passed to the timer function mostly"""
    X,Y = dims
    arr = inp.reshape((-1,Y,X))
    if debugging:
        print(np.array(arr[:]==0, dtype=int))
        print(np.sum(np.array(arr[:]==0, dtype=int),axis=(1,2)))
        print(np.argmin(np.sum(np.array(arr[:]==0, dtype=int),axis=(1,2))))
    z = np.argmin(np.sum(np.array(arr[:]==0, dtype=int),axis=(1,2)))
    if debugging:
        print()
        print(arr[z,:,:])
        print(np.array(arr[z,:,:] == 1,dtype=int))
        print(np.array(arr[z,:,:] == 2,dtype=int))
        print()
    ones = np.sum(np.array(arr[z,:,:] == 1,dtype=int))
    twos = np.sum(np.array(arr[z,:,:] == 2,dtype=int))
    return ones * twos

@ Timer
def part2(inp, dims, debugging=False, **args):
    """ inp = input; **args contains named arguments to be passed to the timer function mostly"""
    X,Y = dims
    out = np.ones((Y,X), dtype=int)*2
    if debugging:
        print(out)
        print()
    arr = inp.reshape((-1,Y,X))
    for z in range(arr.shape[0]):
        w = np.array(out==2,dtype=int) + np.array(out!=arr[z],dtype=int)
        out[w==2] = arr[z,:,:][w==2]
        if debugging:
            print(' w :',w,sep='\n')
            print('out:',out,sep='\n')
            print()
    np_2_str(out)

if __name__ == "__main__":
    """ files needed
        - input.txt
        - test_{x}_input.txt, with x the test number"""
    t0 = time()
    test = 0; prnt = test != 0
    dims = [
        [25,6],
        [3,2],
        [2,2]
    ]
    inp = parse(test, prnt=prnt)
    part1(inp, dims[test], prnt=True)
    part2(inp, dims[test], prnt=True)
    print(f"Total time: {time()-t0}")