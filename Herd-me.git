import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parameters
N = 400  # Total population
infection_seed = 5  # Initial infected individuals
transmission_rate = 0.05  # Probability of infection
recovery_rate = 0.02  # Probability of recovery
waning_immunity_rate = 0.01  # Probability of losing immunity

# State Encoding
SUSCEPTIBLE = 0
INFECTED = 1
RECOVERED = 2

# Initialize population states
states = np.full(N, SUSCEPTIBLE)
infected_indices = np.random.choice(N, infection_seed, replace=False)
states[infected_indices] = INFECTED

# Positioning individuals randomly in space
positions = np.random.rand(N, 2)

# Simulation update function
def update(frame):
    global states
    new_states = states.copy()
    
    for i in range(N):
        if states[i] == SUSCEPTIBLE:
            # Check for infection
            for j in range(N):
                if states[j] == INFECTED:
                    distance = np.linalg.norm(positions[i] - positions[j])
                    if distance < 0.1 and np.random.rand() < transmission_rate:
                        new_states[i] = INFECTED
                        break
        elif states[i] == INFECTED:
            # Recovery
            if np.random.rand() < recovery_rate:
                new_states[i] = RECOVERED
        elif states[i] == RECOVERED:
            # Losing immunity
            if np.random.rand() < waning_immunity_rate:
                new_states[i] = SUSCEPTIBLE
    
    states = new_states
    scatter.set_array(states)
    return scatter,

# Set up the figure
fig, ax = plt.subplots()
scatter = ax.scatter(positions[:, 0], positions[:, 1], c=states, cmap='coolwarm', vmin=0, vmax=2)
ax.set_xticks([])
ax.set_yticks([])
ax.set_title("SIRS Epidemic Simulation")

# Run the animation
ani = animation.FuncAnimation(fig, update, frames=100, interval=100, blit=True)
plt.show()

