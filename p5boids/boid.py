from p5 import Vector, stroke, circle
import numpy as np
import time

class Boid():

    def __init__(self, x, y, width, height, max_speed):
        self.position = Vector(x, y)
        vec = (np.random.rand(2) - 0.5)*1
        self.velocity = Vector(*vec)

        self.max_speed = max_speed
        #self.test = test
        self.perception = 100

        vec = (np.random.rand(2) - 0.5)/10
        self.acceleration = Vector(*vec)

        self.width = width
        self.height = height


    def update(self):
        self.position += self.velocity
        self.velocity += self.acceleration

        if np.linalg.norm(self.velocity) > self.max_speed:
            self.velocity = 5

        #self.velocity.limit(5)

    def show(self):
        stroke(255)
        circle((self.position.x, self.position.y), radius=10)

    def apply_rules(self, boids):
        alignment = self.align(boids)
        print(alignment, self.acceleration)
        #self.acceleration += alignment

    def edges(self):
        if self.position.x > self.width:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = self.width

        if self.position.y > self.height:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = self.height

    def align(self, boids):
        # config
        steering = Vector(0.00, 0.00, 0.00)
        perception = 150
        percepted = 0
        avg_vec = Vector(0.00, 0.00, 0.00)
        # percept
        for boid in boids:
            if np.linalg.norm(boid.position - self.position) < self.perception:
                avg_vec += boid.velocity
                percepted += 1
        if percepted > 0:
            pass
        # get the vector of boid

        # get average vector of boids in a 150 pixel by 150 pixel square
        # steer towards that vector
        pass

