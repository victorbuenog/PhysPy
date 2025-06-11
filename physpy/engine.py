from .utils import Body, Plotter
import numpy as np

class Engine:
    def __init__(self, bodies = [], physics = [], n_dimensions = 3, t_max = 100):
        self.bodies = bodies
        self.time = np.linspace(0, t_max, 1000)
        self.n_dimensions = n_dimensions
        self.physics = physics
        self.time_step = self.time[1] - self.time[0]

    def run(self):
        if "dynamics" in self.physics:
            for t in self.time:
                for body in self.bodies:
                    self.motion(body)
                    body.logger(t)

        plotter = Plotter(self.bodies, self.n_dimensions)
        plotter.plot_trajectory()   

    def forces(self, body):
        forces = np.zeros(self.n_dimensions)

        # Calculate gravity forces
        if "gravity" in self.physics:
            for body2 in self.bodies:
                if body2 != body:
                    forces += self.f_gravity(body, body2)

        # Calculate electric forces
        if "electric" in self.physics:
            for body2 in self.bodies:
                if body2 != body:
                    forces += self.f_electric(body, body2)

        return forces

    def motion(self, body):
        forces = self.forces(body)
        body.force = forces
        body.acceleration = body.acceleration + forces / body.mass
        body.velocity = body.velocity + body.acceleration * self.time_step
        body.position = body.position + body.velocity * self.time_step


    def f_gravity(self, body1, body2):
        G = 6.67430e-11 # Gravitational constant

        distance = np.linalg.norm(body1.position - body2.position)
        force = -G * body1.mass * body2.mass / distance**2

        # Convert to vector
        force = force * (body1.position - body2.position) / distance
        return force
    
    def f_electric(self, body1, body2):
        k = 8.9875517923e9 # Coulomb's constant
        distance = np.linalg.norm(body1.position - body2.position)
        force = k * body1.charge * body2.charge / distance**2

        # Convert to vector
        force = force * (body1.position - body2.position) / distance
        return force