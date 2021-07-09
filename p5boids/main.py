from p5 import setup, draw, size, background, run, Vector
import numpy as np
from boid import Boid

width = 1000
height = 1000
test = Vector(0, 0, 0)

flock = [Boid(*np.random.rand(2)*1000, width, height, 5) for _ in range(100)]

def setup():
    #this happens just once
    size(width, height) #instead of create_canvas



def draw():
    #this happens every time
    background(30, 30, 47)

    for boid in flock:
        boid.edges()
        boid.apply_rules(flock)
        boid.show()
        boid.update()


run()