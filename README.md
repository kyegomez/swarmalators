![Agora banner](agorabanner.png)


# Swarmalator 

Swarmalators are a hybrid swarm oscillator system, combining features of both swarming (particles that align their spatial motion) and oscillators (units that synchronize their phase). This repository provides an implementation of the swarmalator model in a 3D environment using PyTorch.


# Install
`pip install swarmalator`

# Usage
There are 2 verisons, a verison close to the original paper's implementation and a very experimental verison with attn.

- Implementation From paper, with a cool animation

```python
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from swarmalator import simulate_swarmalators

# Example usage:
N = 100
J, alpha, beta, gamma, epsilon_a, epsilon_r, R = [0.1] * 7
D = 3  # Ensure D is an integer
xi, sigma_i = simulate_swarmalators(
    N, J, alpha, beta, gamma, epsilon_a, epsilon_r, R, D
)
print(xi[-1], sigma_i[-1])


def visualize_swarmalators(results_xi):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection="3d")

    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_zlim(-2, 2)

    # Initialize the scatter plot
    scatter = ax.scatter([], [], [])

    def init():
        scatter._offsets3d = ([], [], [])
        return (scatter,)

    def update(num):
        ax.view_init(30, 0.3 * num)
        x_data, y_data, z_data = results_xi[num].t()
        scatter._offsets3d = (x_data, y_data, z_data)
        return (scatter,)

    ani = FuncAnimation(fig, update, frames=len(results_xi), init_func=init, blit=False)

    plt.show()


# Call the visualization function
visualize_swarmalators(xi)
```

- Implementation with attn, params could use tuning, with a visualization suite as well
```python
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
```

## Overview

At the heart of the model are two main components for each swarmalator: 
1. **Spatial Position (`xi`)**: Represents where the swarmalator is in a 3D space.
2. **Phase/Orientation (`sigma_i`)**: Defines the state or phase of the swarmalator.

The dynamics of each swarmalator are driven by interactions with its neighbors. These interactions are based on their relative spatial distances and differences in their phases.

## Dynamics Explained

The dynamics of the swarmalators are governed by two main equations:

1. For the spatial position (`xi`):
    - Swarmalators are attracted or repelled based on the difference in their phases.
    - They also experience a self-propelling force and a damping on high velocities.
  
2. For the phase/orientation (`sigma_i`):
    - The phase changes based on the relative spatial positioning of the swarmalators.
    - There's also an intrinsic phase precession and a nonlinearity which can cause the phase to wrap around.

Using the Runge-Kutta 4th order method (RK4), the system numerically integrates these dynamics over time, leading to the emergent behaviors of the swarmalators.

## Visualization

In the visualization, you will witness:
- A 3D cube that encapsulates the world of swarmalators.
- `N` points inside this 3D space, each representing a swarmalator. The movements and dynamics of these swarmalators are based on the aforementioned interactions.
- A mesmerizing dance of points as they evolve over time, showcasing various patterns, clusters, or scattered behaviors.

## Parameters

The behavior of swarmalators can be fine-tuned using several parameters:
- `N`: Number of swarmalators.
- `J, alpha, beta, gamma, epsilon_a, epsilon_r, R`: Parameters that govern the strength and nature of interactions and dynamics.
- `D`: Dimensionality of the phase/orientation.

## Usage

To simulate the swarmalators, adjust the parameters as desired and run the provided script. Post-simulation, the final positions and phases of the swarmalators are printed, and the visualization can be observed.

```python
N = 100
J, alpha, beta, gamma, epsilon_a, epsilon_r, R = [0.1]*7
D = 3
xi, sigma_i = simulate_swarmalators(N, J, alpha, beta, gamma, epsilon_a, epsilon_r, R, D)
print(xi[-1], sigma_i[-1])
```

## Conclusion

Swarmalators provide a unique and intriguing insight into systems that exhibit both swarming and synchronization behaviors. By studying and visualizing such models, we can gain a better understanding of complex systems in nature and potentially apply these insights to engineering and technological domains.



# Citation
```bibtex
@misc{2308.03803,
Author = {Akash Yadav and Krishnanand J and V. K. Chandrasekar and Wei Zou and Jürgen Kurths and D. V. Senthilkumar},
Title = {Exotic swarming dynamics of high-dimensional swarmalators},
Year = {2023},
Eprint = {arXiv:2308.03803},
}

```