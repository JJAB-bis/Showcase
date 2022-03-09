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



class Robot:
    def __init__(self, brain):
        self.comp  = brain.copy()

        self.x         = 0
        self.y         = 0
        self.direction = 0
        self.direction_map = {
            0 : ( 1, 0),
            1 : ( 0, 1),
            2 : (-1, 0),
            3 : ( 0, -1)
        }
        {i:each for i,each in enumerate('^<v>')}

        self.hull = {(self.y,self.x) : 0}

    
    def rotate(self, i:0|1):
        self.direction = (self.direction + ((i*2)-1)) % 4

    def run(self, starting_color:0|1):
        self.hull = {(self.y,self.x) : starting_color}
        self.brain = self.comp.run(status_updates=False)
        next(self.brain)
        self.brain.send(self.hull[(self.y,self.x)])
        i = 0
        while self.comp.running:
            # print(self.hull.keys())
            color, rotate = self.comp.get_out(2)

            self.hull[(self.y,self.x)] = color
            self.rotate(rotate)
            dy,dx = self.direction_map[self.direction]
            self.y += dy
            self.x += dx
            try:
                self.hull[(self.y,self.x)]
            except:
                self.hull[(self.y,self.x)] = 0
            
            self.brain.send(self.hull[(self.y,self.x)])
        print(len(self.hull.keys()))













@ Timer
def part1(comp, **args):
    """ inp = input; **args contains named arguments to be passed to the timer function mostly"""
    robot = Robot(comp)
    robot.run(starting_color=0)

@ Timer
def part2(comp, goal=None, **args):
    """ inp = input; **args contains named arguments to be passed to the timer function mostly"""
    robot = Robot(comp)
    robot.run(starting_color=1)

    hull = robot.hull
    mx,MX = 0,0
    my,MY = 0,0
    for y,x in hull.keys():
        mx = min(mx,x)
        my = min(my,y)
        MX = max(MX,x)
        MY = max(MY,y)
    
    MY += 1
    MX += 1
    painting = [[' 'for x in range(mx,MX)] for y in range(my,MY)]

    for (y,x), color in hull.items():
        y+=abs(my)
        x+=abs(mx)
        if color:
            painting[y][x] = '#'



    out = '\n'.join( [' '.join(row) for row in reversed(painting)] )
    # out = out.replace('# #', '##')
    print(out)


            


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