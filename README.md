# Swarmulator: A Swarm Simulation with Transformer Architecture

## Table of Contents
- Introduction
- Swarmulator Architecture
- Algorithmic Pseudocode
- Usage
- Conclusion

## Introduction
The Swarmulator is a computational model designed to simulate the behavior of a swarm of agents using modern attention-based Transformer architecture. Each agent in the swarm has a position (`xi`) and orientation (`oi`). The model incorporates interactions between the agents to dynamically evolve their states over time.

## Swarmulator Architecture

### Basic Components:

1. **State Variables**:
    - `xi`: Represents the position of the agent in a `D` dimensional space.
    - `oi`: Represents the orientation of the agent.

2. **Transformer Components**:
    - **Attention Mechanism**: Uses multi-head attention to compute the evolution of the agents based on their interactions with each other.

### Initialization:
The Swarmulator class is initialized with several parameters:

- `D`: The dimensionality of the agents. It defines the space in which the agents exist.
- `heads`: The number of heads in the multi-head attention mechanism.
- `N`: The number of agents in the swarm.
- Other parameters influencing the behavior and interactions of the agents include `J`, `a`, `β`, `y`, `εa`, `εr`, and `R`.

Upon initialization, random positions and orientations are assigned to each agent. The attention mechanisms specific to position (`xi`) and orientation (`oi`) are also set up.

### Transformer Integration:
To model the interactions between agents, we utilize the transformer's attention mechanism. The idea is to allow each agent to 'pay attention' to other agents when deciding its next state. This is implemented using the multi-head attention mechanism from the Transformer architecture.

For positions (`xi`) and orientations (`oi`), we have distinct attention mechanisms, thus allowing the system to model different interaction dynamics for position and orientation.

## Algorithmic Pseudocode

```
Class Swarmulator:
    
    INIT(D, heads, N, J, a, β, y, εa, εr, R):
        Set state dimensions, D
        Set number of agents, N
        Initialize agent-specific parameters: J, a, β, y, εa, εr, R
        Initialize agent states: xi, oi
        
        Setup attention mechanisms for xi and oi

    FUNCTION evolution_of_xi:
        Use attention mechanism on xi
        RETURN updated xi

    FUNCTION evolution_of_oi:
        Use attention mechanism on oi
        RETURN updated oi

    FUNCTION RK4_step(y, evolution_func, dt):
        Compute k1, k2, k3, k4 using the evolution function
        UPDATE y based on the computed values
        RETURN y

    FUNCTION simulation(num_steps):
        FOR each step in num_steps:
            UPDATE xi using RK4_step
            UPDATE oi using RK4_step
            Normalize oi

END Class

```

## Usage

### Initialization:

To initialize the Swarmulator, provide the required parameters. For instance:

```python
swarm = Swarmulator(N=100, D=3, heads=4)
```

This initializes a swarm with 100 agents in a 3-dimensional space using an attention mechanism with 4 heads.

### Running a Simulation:

To run the simulation for a certain number of steps:

```python
swarm.simulation(num_steps=1000)
```

You can then access the final positions and orientations of the agents using:

```python
print(swarm.xi)
print(swarm.oi)
```

## Conclusion

Swarmulator offers a unique approach to simulating swarm dynamics by integrating modern attention-based mechanisms from the Transformer architecture. This allows the model to capture complex interactions between agents in a computationally efficient manner. Whether you're researching swarm behaviors, designing swarm robotics, or just curious about the application of Transformer architectures in unconventional scenarios, Swarmulator provides a robust framework to kickstart your experiments.

