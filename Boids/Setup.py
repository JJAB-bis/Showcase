import random as r
import numpy as np

import ctypes
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

"""
Centeralization of all parameters
dictionary with keys:
    uni  : handels universe specific setup
    anim : handels animation specific setup
    boid : handels boid specific setup
settings in anim should not matter to uni or boid
"""

setup_dict = {
    'uni': {
        'dims'      : np.array((screensize[0],screensize[1])),
        'dim_bound' : 100,
        'boids'     : 100,
        'anim'      : True
    },
    'anim' : {
        'scale'  : 1,
        'tick'   : 600,
        'screen' : {
            'bg' : (100,100,100)
        },
        'grid':  {
            'color'   : 'grey',
            'outline' : '',
            'width'   : '1'
        },
        'tree' :{
            'anim_tree'  : False,
            'colour'     : (60,0,0),
            'thickness'  : 2
        },
        'boid' : {
            'color'      : lambda : np.random.randint(0,256,3),
            'area_color' : (200,200,200),
            'outline'    : 'black',
            'rad'        : 10
        
        }
    },
    'boid' : {
        'start' : 'const_vel',
        'stats' : {
            'set'       : lambda : np.vstack(((100.,100.),(-1,-1),(0,0.001))),
            'still'     : lambda : np.vstack((np.random.rand(2), (0,0), (0,0))),
            'const_vel' : lambda : np.vstack((np.random.rand(2), np.random.uniform(-0.1,0.1,[2]), (0,0))),
            'const_acc' : lambda : np.vstack((np.random.rand(2), np.random.uniform(-0.5,0.5,[2]), np.random.uniform(-0.5,0.5,[2])))
            },
        'max_vel'     : 10,
        'max_acc'     : 1,
        'forces' : {
            'seperation' : {
                'size'   : 60,
                'radius' : 40,
                'apply'  : True
                },
            'alignment' : {
                'size'   : 40,
                'radius' : 60,
                'apply'  : True
                },
            'cohesion' : {
                'size'   : 30,
                'radius' : 30,
                'apply'  : True
                },
            }
    }
}



if __name__ == "__main__":
    # call the simulation from main
    from Main import Universe
    uni = Universe()
    uni.start()