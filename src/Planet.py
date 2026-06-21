import numpy as np
#import Simulation as sim

G = 1.0 # Gravitational Constant (tunable)
dt = 0.1  # Time step for integration (smaller -> more accurate)

"""
Class to define celestial bodies
"""
class Planet:
    """
    Initialize a planet.
    """
    def __init__(self, name, x_coord, y_coord, mass, vx, vy, size):
        self.name = name
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.mass = mass
        self.vx = vx  
        self.vy = vy  
        self.size = size
    def update(self, bodies):
        # Use velocity-Verlet integration for improved energy behaviour
        # 1) compute accelerations at current positions
        forces = self.compute_forces(bodies)
        accs = [(fx / b.mass, fy / b.mass) for (fx, fy), b in zip(forces, bodies)]

        # 2) update positions using current velocities and accelerations
        for b, (ax, ay) in zip(bodies, accs):
            b.x_coord += b.vx * dt + 0.5 * ax * (dt ** 2)
            b.y_coord += b.vy * dt + 0.5 * ay * (dt ** 2)

        # 3) compute new accelerations at updated positions
        forces_new = self.compute_forces(bodies)
        accs_new = [(fx / b.mass, fy / b.mass) for (fx, fy), b in zip(forces_new, bodies)]

        # 4) update velocities with the average acceleration
        for b, (ax, ay), (axn, ayn) in zip(bodies, accs, accs_new):
            b.vx += 0.5 * (ax + axn) * dt
            b.vy += 0.5 * (ay + ayn) * dt

            # if body.x_coord >= sim.WINDOW_WIDTH or body.x_coord <= 0:
            #     body.vx = -body.vx
            # if body.y_coord >= sim.WINDOW_HEIGHT or body.y_coord <= 0:
            #     body.vy = -body.vy

    def compute_forces(self, bodies):
        forces = [(0,0) for _ in bodies]
        for i, b1 in enumerate(bodies):  # Loop over each body experiencing force
            fx, fy = 0.0, 0.0  # Net force components for b1
            for j, b2 in enumerate(bodies):  # Loop over bodies exerting force
                if i != j:  # Avoid self-interaction
                    dx = b2.x_coord - b1.x_coord  # Difference in x-coordinates
                    dy = b2.y_coord - b1.y_coord  # Difference in y-coordinates
                    dist = (dx**2 + dy**2)**0.5 + 1e-10  # Compute distance (avoid division by zero)
                
                    force_mag = G * b1.mass * b2.mass / dist**2  # Newton's law
                    # print(f"force_mag: {force_mag}")
                    # print(f"dist: {dist}")
                    # print(f"dx: {dx}")
                    # print(f"dy: {dy}")
                    # Compute force components in x and y directions
                    fx += force_mag * (dx / dist)  
                    fy += force_mag * (dy / dist)

                    forces[i] = (fx, fy)  # Store computed force for this body

        return forces
