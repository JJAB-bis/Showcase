
import numpy as np
import random as R

class Node:
    def __init__(self, y,x, allowed):
        self.y = y
        self.x = x
        self.allowed = np.ones((allowed), dtype=int)
        self.tilekey = -1
        self.neighbours = {i:None for i in range(4)}

    def set_key(self, choice:[int]):
        self.allowed *= 0
        self.allowed[choice[0]] = 1
        self.tilekey = choice[0]
        return choice

    def set_random_key(self):
        choice = self.random_allowed()
        return self.set_key(choice)

    def random_allowed(self):
        p = self.allowed==1
        p = p/sum(p)
        return np.random.choice(self.allowed.shape[0],size=1, p=p)

    def connect(self, poss, others):
        for each, ds in poss:
            if each in others:
                do = (ds+2)%4
                self.neighbours[ds] = others[each]
                others[each].neighbours[do] = self

    def update_allowed(self, conn):
        for ds, node in self.neighbours.items():
            if node is None or node.tilekey==-1:
                continue
            self.allowed=np.bitwise_and(self.allowed, conn[node.allowed==1,:].flatten())

    def __repr__(self):
        return f"({self.y},{self.x},{self.tilekey})"


class World:
    def __init__(self, W=20,H=20):
        self.W = W
        self.H = H
        # sea, shore, plain, mountain, forrest
        self.conn = np.array([
        [1,1,0,0,0], # sea
        [1,1,1,1,0], # shore
        [0,1,1,1,1], # plain
        [0,1,1,0,0], # mountain
        [0,0,1,0,1], # forrest
        ], dtype=int)
        assert self.conn.shape[0] == self.conn.shape[1]
        self.allowed_n = self.conn.shape[0]

    def neighbours(self, node):
        y,x = node.y,node.x
        if y+1 <  self.H: yield (y+1,x), 0
        if x+1 <  self.W: yield (y,x+1), 1
        if y >= 1:        yield (y-1,x), 2
        if x >= 1:        yield (y,x-1), 3

    @staticmethod
    def lim_filter(x):
        return np.sum(x.allowed)

    def find_limited(self):
        if len(self.active) == 0: raise Exception("No more active nodes")
        lim = min(map(self.lim_filter,self.active))
        for node in self.active:
            if self.lim_filter(node) == lim:
                return node

    def gen_neighbours(self, node):
        keys = set(self.nodes.keys())
        for pos, d in self.neighbours(node):
            if not pos in keys:
                new_node = Node(*pos, self.allowed_n)
                self.nodes[pos] = new_node
                self.active.add(new_node)
                new_node.connect(self.neighbours(new_node), self.nodes)
            self.nodes[pos].update_allowed(self.conn)

    def run(self):
        m = (self.H//2, self.W//2)
        current = Node(*m, self.allowed_n)
        self.nodes={}; self.nodes[m] = current
        self.active = {current} # +1 because it's a len index
        for _ in range(self.H*self.W):
            current = self.find_limited()
            choice = current.set_random_key()
            #choice = current.set_key([0])
            self.gen_neighbours(current)
            self.active.remove(current)

        print(len(self.nodes.keys()))

    def map_2_array(self):
        out = np.zeros((self.H,self.W), dtype=int)
        for pos, node in self.nodes.items():
            out[pos] = node.tilekey
        return out


    def __repr__(self):
        return str(self.map_2_array())


if __name__ == '__main__':
    w = World()
    w.run()
    print(w)
