from Setup import setup_dict as sd
from Anim  import Anim
from Boid  import Boid
from QTree import QTree

import time
import numpy as np

class Universe:
    """ Controler for the simulation """
    def __init__(self, setup_dict=None):
        self.setup_dict = setup_dict if setup_dict != None else sd
    
    def start(self):
        """ runs simulation """
        print(self.setup_dict, '\n')
        self._setup() 
        self.boids = [Boid(self) for _ in range(self.n_boids)]

        if self.anim: # allows the simulation to run without animation
            self.anim = Anim(self).run()
            next(self.anim)
            self.anim.send(self.boids)
        max_updates = 1000 if not self.anim else None
        updates = 0
        while True: # update loop
            qtree = QTree(self.boids, self.dims, 1) # spactial partioning to decrease O(n^2) -> O(nlogn)
            for boid in self.boids:
                boid.update(qtree)
            if self.anim:
                try:
                    self.anim.send((self.boids, qtree))
                except Exception as e:
                    print(f"Exception: {e}")
                    break
            if max_updates != None: # if no animation is made, the loop would be infinite
                updates += 1
                if updates > max_updates :
                    break
        if self.anim: #
            self._exit()

    def _setup(self):
        """ handels extraction of variabls from setup file """
        setup = self.setup_dict['uni']
        self.dims    = setup['dims']
        self.dims   -= setup['dim_bound']
        self.n_boids = setup['boids']
        self.anim    = setup['anim']

        # apply selection off forces to be used to avoid unnecesary copmutations down the line
        for force in list(self.setup_dict['boid']['forces'].keys()):
            self.setup_dict['boid']['forces'][force]['radius'] +=  self.setup_dict['anim']['boid']['rad'] if self.anim else 0
            if not self.setup_dict['boid']['forces'][force]['apply']:
                self.setup_dict['boid']['forces'].pop(force,0)
        self.setup_dict['boid']['scale_arr'] = np.array(
            [[self.setup_dict['boid']['forces'][force]['size']] for force in self.setup_dict['boid']['forces']],
        )
        # ---


    def _exit(self):
        """ ensures proper closure of pygame """
        self.anim.close()

if __name__ == "__main__":
    universe = Universe()
    universe.setup_dict
    universe.start()