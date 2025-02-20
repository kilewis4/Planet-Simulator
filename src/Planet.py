import numpy as np

G = 6 # Gravitational Constant
dt = 1       # Time Step  

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
        forces = self.compute_forces(bodies)  # Get force tuples (fx, fy)
        print(f"forces: {forces}")
    
        for i, body in enumerate(bodies):
            fx, fy = forces[i]  # Extract force components
            #sprint(f"forces[i]: {forces[i]}")


            # Compute acceleration in x and y directions
            ax = fx / body.mass  
            ay = fy / body.mass  

            # Update velocity components
            body.vx += ax * dt  
            body.vy += ay * dt  

            print(f"body.vx: {body.vx}")
            print(f"body.vy: {body.vy}")

            # Update position components
            body.x_coord += (body.vx * dt)   
            body.y_coord += (body.vy * dt) 

            if body.x_coord >= 1250 or body.x_coord <= 0:
                body.vx = -body.vx
            if body.y_coord >= 700 or body.y_coord <= 0:
                body.vy = -body.vy

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
                    print(f"force_mag: {force_mag}")
                    print(f"dist: {dist}")
                    print(f"dx: {dx}")
                    print(f"dy: {dy}")
                    # Compute force components in x and y directions
                    fx += force_mag * (dx / dist)  
                    fy += force_mag * (dy / dist)

                    forces[i] = (fx, fy)  # Store computed force for this body

        return forces
