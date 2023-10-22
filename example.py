import torch
from swarmalator import Swarmulator


# Initialize the Swarmulator
N = 100  # Number of agents
D = 100  # Dimensionality of agents
swarm = Swarmulator(N=N, D=D, heads=5)

# Run a simple forward pass
swarm.simulation(num_steps=10)

# Print the final positions and orientations of the swarm agents
print("Final positions (xi) of the agents:")
print(swarm.xi)
print("\nFinal orientations (oi) of the agents:")
print(swarm.oi)
