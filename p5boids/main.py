from p5 import *
import numpy as np
from boid import Boid
from bead import Bead
import os
from threading import Thread
from dash_testing import value

print(value)

width = 1000
height = 1000


# set up the two flocks of birds
flock = [Boid(*np.random.rand(2)*1000, width, height, 10) for _ in range(15)]
beads = [Bead(*np.random.rand(2)*1000, width, height, 10) for _ in range(15)]

def setup():
    size(width, height) # this creates the canvas (the setup function is only ran once)

def draw():
    background(30, 30, 47)

    # the draw function runs every frame (it is set to 30 fps)

    for boid in flock:
        boid.edges()
        boid.apply_rules(flock, beads)
        boid.show()
        boid.update()

    for bead in beads:
        bead.edges()
        bead.apply_rules(beads, flock)
        bead.show()
        bead.update()

#if __name__ == '__main__':
#    run(frame_rate=30)


