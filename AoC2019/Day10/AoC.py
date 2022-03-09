#-*-coding:utf8;-*-
#qpy:3
#qpy:console

def pprint(inp:iter) -> None:
    print("[")
    for i in inp:
        print(i)
    print("]")
n = '\n'

import math

import numpy as np


class Station:
    def __init__(self, smap:str):
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
        return pos
                
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
            

if __name__ == "__main__":
    inp =".#..#. ...... #####. ....#. ...##."
    # inp ="......#.#. #..#.#.... ..#######. .#.#.###.. .#..#..... ..#....#.# #..#....#. .##.#..### ##...#..#. .#....####"
    inp = ".#....#####...#.. ##...##.#####..## ##...#...#.#####. ..#.....#...###.. ..#.#.....#....##"
    inp=".###.###.###.#####.# #####.##.###..###..# .#...####.###.###### ######.###.####.#### #####..###..######## #.##.###########.#.# ##.###.######..#.#.# .#.##.###.#.####.### ##..#.#.##.######### ###.#######.###..##. ###.###.##.##..####. .##.####.##########. #######.##.###.##### #####.##..####.##### ##.#.#####.##.#.#..# ###########.#######. #.##..#####.#####..# #####..#####.###.### ####.#.############. ####.#.#.##########."
    
    
    test = Station(inp)
    # y,x  = 18,8    
    y,x = test.scan()
    print(test.vaporize(y,x))

    # 502 == ans > 205



#
