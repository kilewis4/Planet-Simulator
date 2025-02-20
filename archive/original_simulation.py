import numpy as np
import matplotlib.pyplot as plt

# Constants
G = 6.67430e-11  # Gravitational constant
dt = 1000  # Time step (seconds)

# Bodies: [mass, x, y, vx, vy]
bodies = np.array([
    [1.989e30, 0, 0, 0, 0],  # Sun
    [5.972e24, 1.496e11, 0, 0, 29780],  # Earth
    [7.348e22, 1.496e11 + 3.844e8, 0, 0, 29780 + 1022]  # Moon
])

# Simulation parameters
steps = 10000
positions = np.zeros((steps, len(bodies), 2))  # Store positions for plotting

# Simulation loop
for step in range(steps):
    positions[step] = bodies[:, 1:3]  # Store current positions
    for i in range(len(bodies)):
        total_force = np.zeros(2)
        for j in range(len(bodies)):
            if i != j:
                r = bodies[j, 1:3] - bodies[i, 1:3]
                distance = np.linalg.norm(r)
                force_magnitude = G * bodies[i, 0] * bodies[j, 0] / distance**2
                force = force_magnitude * (r / distance)
                total_force += force
        # Update velocity and position
        bodies[i, 3:5] += (total_force / bodies[i, 0]) * dt
        bodies[i, 1:3] += bodies[i, 3:5] * dt

# Plot the orbits
plt.figure(figsize=(10, 10))
for i in range(len(bodies)):
    plt.plot(positions[:, i, 0], positions[:, i, 1], label=f'Body {i+1}')
plt.scatter(bodies[:, 1], bodies[:, 2], color='black')  # Final positions
plt.legend()
plt.xlabel('x (m)')
plt.ylabel('y (m)')
plt.title('Orbits of Celestial Bodies')
plt.show()