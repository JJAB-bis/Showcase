import random as r
import numpy as np
import copy

class Point:
    def __init__(self, data):
        """ small class used to represent the boids. It copies the positional data so that all the boids are updated with the same dataset """
        try:
            self.x,self.y = data.x, data.y 
        except AttributeError: # usefull for debugging and more general application of code
            self.x,self.y = data.pos[0]
        self.data = copy.deepcopy(data.pos)

class Rect:
    def __init__(self, cx, cy, w, h):
        """
            (0,0) ##### self.north_edge ##### (w,0)\n
            #                  |                  #\n
            #                  |                  #\n
            self.west_edge--(cx,cy)--self.east_edge\n
            #                  |                  #\n
            #                  |                  #\n
            (0,h) ##### self.south_edge ##### (w,h) """
        self.cx, self.cy = cx, cy
        self.w,  self.h  = w,  h

        self.north_edge, self.south_edge = cy - h/2, cy + h/2
        self.east_edge,  self.west_edge  = cx + w/2, cx - w/2

    def is_inbounds(self, point):
        """ checks if a point is within the edges """
        try:
            x,y = point.x, point.y
        except AttributeError:
            x,y = point
        return (
            self.east_edge  > x >= self.west_edge  and
            self.south_edge > y >= self.north_edge
            )
    
    def intersect(self, other):
        """ checks if any edges overlap """
        return not (
            other.north_edge > self.south_edge or
            other.south_edge < self.north_edge or
            other.east_edge  < self.west_edge  or
            other.west_edge  > self.east_edge
        )

class QTree:
    """ constructor wrapper around tradional branch/qtree recursive algorithem """
    def __init__(self, data_list, dims, max_points=4):
        """ takes a list of boids or points, 
            initiates qtree, 
            inserts all boids into qtree,
            checks if all points were succesfully inserted """
        # TODO handel case's where boids overlap, currently causes problem similar to passing recursion depth

        data_list = [Point(elem) for elem in data_list] # use Point rather than the boids to 'freeze' their positions per timestep
        w,  h  = dims
        cx, cy = w/2, h/2
        tree = Branch(
            Rect(cx, cy, w, h),
            max_points
        )
        missed = set()
        for elem in data_list:
            if not tree.insert(elem):
                missed.add(elem)
        if len(missed) > 0:
            raise ValueError( f"Point{'s were' if len(missed) > 1 else ' was'} not inserted:\n - " + '\n - '.join(map(str,missed)))
        self.tree = tree

    def query(self, point, r, found):
        """ querys qtree around point """
        # TODO circular/pie area querry, add distance/angle calc to returned points?
        cx,cy = point
        rect = Rect(cx,cy,r,r)
        return self.tree.query(rect, found)

class Branch:
    def __init__(self, rect, max_points=4, depth=0):
        """ recursive structure that takes points,
            if more points are given than allowed devide
            """
        self.points     = []
        self.rect       = rect
        self.depth      = depth
        self.max_points = max_points
        self.devided    = False
    
    def devide(self):
        """
            (0,0) ##### self.north_edge ##### (w,0)\n
            #                  |                  #\n
            #                  |                  #\n
            self.west_edge--(cx,cy)--self.east_edge\n
            #                  |                  #\n
            #                  |                  #\n
            (0,h) ##### self.south_edge ##### (w,h) """

        cx,cy = self.rect.cx,  self.rect.cy
        w, h  = self.rect.w/2, self.rect.h/2
        self.quad_NE = Branch( Rect(cx+w/2,cy-h/2, w,h), self.max_points, self.depth+1 )
        self.quad_SE = Branch( Rect(cx+w/2,cy+h/2, w,h), self.max_points, self.depth+1 )
        self.quad_SW = Branch( Rect(cx-w/2,cy+h/2, w,h), self.max_points, self.depth+1 )
        self.quad_NW = Branch( Rect(cx-w/2,cy-h/2, w,h), self.max_points, self.depth+1 )
        self.devided = True

    def insert(self, point):
        """ if the point belongs in this rect 
            -> insert it if not yet reaced max points 
            -> devide if not devide 
            -> insert in quarters """
        """
            # TESTS
            print( self.rect.is_inbounds( (10,10) )    == True )
            print( self.rect.is_inbounds( (0,0)   )    == True )
            print( self.rect.is_inbounds( (x,y)   )    == True )
            print( self.rect.is_inbounds( (-1,0)  )    == False )
            print( self.rect.is_inbounds( (0,-1)  )    == False )
            print( self.rect.is_inbounds( (-1,-1) )    == False )
            print( self.rect.is_inbounds( (x+5,y+1))   == False )
            print( self.rect.is_inbounds( (x+0,y+0))   == True )
            print( self.rect.is_inbounds( (x-1,y-1))   == True )
            """
        if not self.rect.is_inbounds(point):
            return False
        elif len(self.points) < self.max_points:
            self.points.append(point)
            return True
        elif not self.devided:
            self.devide()
        return (
            self.quad_NE.insert(point) or
            self.quad_SE.insert(point) or
            self.quad_SW.insert(point) or
            self.quad_NW.insert(point)
        )

    def query(self, other, found):
        """ check if this rect intersects the query
            -> return own points
            -> if devided
            --> return points from children"""
        if not self.rect.intersect(other):
            return False
        for point in self.points:
            if other.is_inbounds(point):
                found.append(point.data)
        if self.devided:
            self.quad_NE.query(other,found)
            self.quad_SE.query(other,found)
            self.quad_SW.query(other,found)
            self.quad_NW.query(other,found)
        return found


if __name__ == "__main__":
    # call the simulation from main
    from Main import Universe
    uni = Universe()
    uni.start()
