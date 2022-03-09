import numpy as np
np.set_printoptions(precision=3)

class Boid:
    def _setup(self, setup):
        """ handels some setup of variables from setup file """
        self.pos     = setup['stats'][setup['start']]() 
        self.pos[0]  = self.pos[0] * self.uni.dims
        
        self.dims    = self.uni.dims
        self.max_vel = setup['max_vel']
        self.max_acc = setup['max_acc']

        self.forces  = setup['forces']
        self.force_functions={
            'seperation' : self.seperation,
            'alignment'  : self.alignment,
            'cohesion'   : self.cohesion 
        }

        self.scale_arr = setup['scale_arr']

    def __init__(self, uni):
        self.uni = uni
        self._setup(uni.setup_dict['boid'])
    
    def _scale_vector(self, v, m = None):
        # if a vector (v) is longer than magnitude (m) shorten it to m
        if m == None:
            return
        norm = np.linalg.norm(v)
        if norm > m:
            v *= m
            v /= norm

    def update(self, qtree):
        """ update velocity and position and limits them """
        self.pos[2]  = self.calc_force(qtree)
        self._scale_vector(self.pos[2], self.max_acc)
        self.pos[1] += self.pos[2]
        self._scale_vector(self.pos[1], self.max_vel)
        self.pos[0] += self.pos[1]
        self.pos[0]  = np.mod(self.pos[0], self.dims) # handels looping out of bounds

    def calc_force(self, qtree):
        """ sets up an array for all the forces that need to be aplied """
        force_arr = np.zeros((len(self.forces),2)) # (forces, dimentions)
        for f, (force, values) in enumerate(self.forces.items()): # loop over the applying forces
            func = self.force_functions[force] # lookup the right functions
            # loop over the point returned from the qtree
            for i, point in enumerate( qtree.query(self.pos[0], values['radius'], [])[1:] ): # first is always the point itself
                force_arr[f] += func(point)
            if force == 'cohesion' and not np.all(force_arr[f] == 0): # cohesion needs an extra step after looping
                force_arr[f] = self.cohesion(force_arr[f], i+1)
        self.normalize(force_arr)
        force_arr[np.isnan(force_arr)] = 0
        return force_arr.sum(axis=0)

    def normalize(self, force):
        """ scales all force vectors to the designated lenght """
        x,_ =  force.shape
        for i in range(x):
            try:
                force[i] /= np.linalg.norm(force[i,:])
            except ZeroDivisionError:
                force[i] = 0
        force *= self.scale_arr

    def cohesion(self, point, m=None):
        """ returns position of the other boids, then returns a vector away from the center mass """
        return point[0] if m == None else (point/m)-self.pos[0]

    def seperation(self, other):
        """ return a vector away from other boids """
        return (self.pos[0] - other[0]) / np.linalg.norm(self.pos[0] - other[0])

    def alignment(self, other):
        """ return the velocity vector of other boids """ 
        return other[1]

    def __repr__(self):
        # a somewhat human readably representation
        return str(self.pos[0])


if __name__ == "__main__":
    # call the simulation from main
    from Main import Universe
    uni = Universe()
    uni.start()