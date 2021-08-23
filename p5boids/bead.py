from p5 import *
import numpy as np

from boid import Boid

class Bead:

    def __init__(self, x, y, width, height, max_speed):
        self.position = Vector(x, y)
        vec = (np.random.rand(2) - 0.5)*10
        self.velocity = Vector(*vec)

        self.max_speed = max_speed
        self.perception = 50

        vec2 = (np.random.rand(2) - 0.5)/2
        self.acceleration = Vector(*vec2)

        self.width = width
        self.height = height

        self.max_force = 0.4

        self.max_power = 1
        self.power = 100


    def update(self):
        self.velocity += self.acceleration
        self.position += self.velocity

        self.velocity.limit(5)
        self.acceleration *= 0

    def show(self):
        stroke(255, 0, 0)
        fill(255, 0, 0)
        circle(self.position.x, self.position.y, 10)

    def apply_rules(self, boids, blue):
        alignment = self.align(boids)
        cohesion = self.cohesion(boids)
        separation = self.separation(boids)
        eww = self.eww(boids, blue)

        self.acceleration += alignment
        self.acceleration += cohesion
        self.acceleration += separation * 3
        self.acceleration += eww * 20
        #print('suf')


        #doodoo = input('inpooot: ')
        #cohesion *= int(doodoo)

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
        steering = Vector(*np.zeros(2))
        total = 0
        sum = Vector(*np.zeros(2))
        for boid in boids:
            if np.linalg.norm(boid.position - self.position) < self.perception:
                sum += boid.velocity
                total += 1

        if total > 0:
            sum /= total
            sum = Vector(*sum)
            sum = (sum / np.linalg.norm(sum)) * self.max_speed
            steering = sum - self.velocity

        return steering

    def cohesion(self, boids):
        total = 0
        com = Vector(*np.zeros(2))
        steering = Vector(*np.zeros(2))
        for boid in boids:
            if np.linalg.norm(boid.position - self.position) < self.perception:
                com += boid.position
                total += 1

        if total > 1:
            com /= total
            com = Vector(*com)
            com_vec = com - self.position
            if np.linalg.norm(com_vec) > 0:
                com_vec = (com_vec / np.linalg.norm(com_vec)) * self.max_speed
            steering = com_vec - self.velocity

            steering.limit(self.max_force)

        return steering

    def separation(self, boids):
        total = 0
        steering = Vector(*np.zeros(2))
        for boid in boids:
            distance = np.linalg.norm(self.position - boid.position)
            if distance < 40 and self.position != boid.position:
                diff = self.position - boid.position
                diff /= distance ** 2
                steering += diff
                total += 1

        if total > 0:
            steering /= total
            if np.linalg.norm(steering) > 0:
                steering = (steering / np.linalg.norm(steering)) * self.max_speed
            steering -= self.velocity
            steering.limit(self.max_force)

        return steering

    def eww(self, boids, blue):
        total = 0
        steering = Vector(*np.zeros(2))

        for boid in blue:
            distance = np.linalg.norm(self.position - boid.position)
            if distance < 80 and self.position != boid.position:
                diff = self.position - boid.position
                diff /= distance ** 2
                steering += diff
                total += 1

            if total > 0:
                steering /= total
                if np.linalg.norm(steering) > 0:
                    steering = (steering / np.linalg.norm(steering)) * self.max_speed
                steering -= self.velocity
                steering.limit(self.max_force)
                #print('success')

        return steering
