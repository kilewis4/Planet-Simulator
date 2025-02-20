import numpy as np
import matplotlib.pyplot as plt

G = 6.67430e-11  # Gravitational constant
dt = 1e4  # Time step (adjust based on scale)
num_steps = 2  # Number of simulation steps

class Body:
    def __init__(self, mass, position, velocity):
        self.mass = mass
        self.position = np.array(position, dtype=np.float64)
        self.velocity = np.array(velocity, dtype=np.float64)

def compute_forces(bodies):
    forces = [np.zeros(2) for _ in bodies]
    for i, b1 in enumerate(bodies):
        for j, b2 in enumerate(bodies):
            if i != j:
                r = b2.position - b1.position
                dist = np.linalg.norm(r) + 1e-10  # Avoid division by zero
                force_mag = G * b1.mass * b2.mass / dist**2
                forces[i] += force_mag * (r / dist)
    return forces

def update(bodies):
    forces = compute_forces(bodies)
    for i, body in enumerate(bodies):
        acceleration = forces[i] / body.mass
        body.velocity += acceleration * dt
        body.position += body.velocity * dt

# Example: Sun-Earth system
bodies = [
    Body(1.989e30, [0, 0], [0, 0]),  # Sun
    Body(5.972e24, [1.5e11, 0], [0, 30000])  # Earth
]

positions = [[] for _ in bodies]
for _ in range(num_steps):
    update(bodies)
    for i, body in enumerate(bodies):
        positions[i].append(body.position.copy())

# Plot the orbits
for pos in positions:
    pos = np.array(pos)
    plt.plot(pos[:, 0], pos[:, 1])
plt.xlabel("X position (m)")
plt.ylabel("Y position (m)")
plt.title("Orbit Simulation")
plt.show()
