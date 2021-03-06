from p5 import *
import numpy as np

class Boid:

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
        stroke(0, 0, 255)
        fill(0, 0, 255)
        circle(self.position.x, self.position.y, 10)

    def apply_rules(self, boids, red):
        # define the acceleration that the rules output
        alignment = self.align(boids)
        cohesion = self.cohesion(boids)
        separation = self.separation(boids)
        eww = self.eww(boids, red)

        # apply the acceleration to the boid's acceleration
        self.acceleration += alignment
        self.acceleration += cohesion
        self.acceleration += separation * 3
        self.acceleration += eww * 20

    def edges(self):
        # if the boid exceeds one of the boundaries the axis' position
        # it exceeded the boundary on will be set to 0
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
                # loop for all the boids to get all the boids within the
                # boids perception radius
                sum += boid.velocity # get all boid's velocities within perception radius
                total += 1 # number of boids within perception

        if total > 0:
            sum /= total
            sum = Vector(*sum)
            sum = (sum / np.linalg.norm(sum)) * self.max_speed # normalize average velocity
            steering = sum - self.velocity # steer boid to average velocity

        return steering

    def cohesion(self, boids):
        # setup
        total = 0
        com = Vector(*np.zeros(2))
        steering = Vector(*np.zeros(2))
        for boid in boids:
            if np.linalg.norm(boid.position - self.position) < self.perception:
                com += boid.position # add all the positions to later get center of mass
                total += 1

        if total > 1:
            com /= total # get average aka center of mass
            com = Vector(*com)
            com_vec = com - self.position # difference between center of mass and boid's position
            if np.linalg.norm(com_vec) > 0:
                com_vec = (com_vec / np.linalg.norm(com_vec)) * self.max_speed # normalize speed
            steering = com_vec - self.velocity # formula for steering

            steering.limit(self.max_force)

        return steering

    def separation(self, boids):
        # setup
        total = 0
        steering = Vector(*np.zeros(2))
        # diff is reversely proportionate to distance (farther a other boid is less the "main" boid will move away from it)
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

    def eww(self, boids, red):
        # function to make two groups of boids
        # setup
        total = 0
        steering = Vector(*np.zeros(2))

        # same as seperation function except larger perception radius
        # red means red boids
        # in main.py red/blue for the other group is set to the opposite's group's flock variable
        for boid in red:
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
