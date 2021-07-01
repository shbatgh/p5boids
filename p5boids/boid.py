from p5 import Vector, stroke, circle
import numpy as np

class Boid():

    def __init__(self, x, y, width, height):
        self.position = Vector(x, y)
        vec = (np.random.rand(2) - 0.5)*10
        self.velocity = Vector(*vec)

        vec = (np.random.rand(2) - 0.5)/2
        self.acceleration = Vector(*vec)

        self.width = width
        self.height = height

    def show(self):
        stroke(255)
        circle((self.position.x, self.position.y), radius=10)

    def update(self):
        self.position += self.velocity
        self.velocity += self.acceleration

    def edges(self):
        if self.position.x > self.width:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = self.width

        if self.position.y > self.height:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = self.height