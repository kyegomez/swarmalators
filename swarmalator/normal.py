import torch


def pairwise_distances(x):
    # Compute pairwise distance matrix
    diff = x.unsqueeze(1) - x.unsqueeze(0)
    return torch.sqrt((diff**2).sum(2))


def function_for_x(xi, sigma_i, N, J, alpha, beta, gamma, epsilon_a, epsilon_r, R, D):
    dists = pairwise_distances(xi)
    mask = (dists < R).float() - torch.eye(N)

    interaction_term = mask.unsqueeze(2) * (sigma_i.unsqueeze(0) - sigma_i.unsqueeze(1))
    interaction_sum = interaction_term.sum(1)

    # Define dynamics for x based on our assumptions
    dx = J * interaction_sum + alpha * xi - beta * (xi**3)
    return dx


def function_for_sigma(
    xi, sigma_i, N, J, alpha, beta, gamma, epsilon_a, epsilon_r, R, D
):
    dists = pairwise_distances(xi)
    mask = (dists < R).float() - torch.eye(N)

    interaction_term = mask.unsqueeze(2) * (xi.unsqueeze(0) - xi.unsqueeze(1))
    interaction_sum = interaction_term.sum(1)

    # Define dynamics for sigma based on our assumptions
    d_sigma = gamma * interaction_sum + epsilon_a * sigma_i - epsilon_r * (sigma_i**3)
    return d_sigma


def simulate_swarmalators(
    N, J, alpha, beta, gamma, epsilon_a, epsilon_r, R, D, T=100, dt=0.1
):
    xi = 2 * torch.rand(N, 3) - 1
    sigma_i = torch.nn.functional.normalize(torch.randn(N, D), dim=1)

    results_xi = []
    results_sigma_i = []

    for t in range(T):
        for i in range(N):
            dx = function_for_x(
                xi, sigma_i, N, J, alpha, beta, gamma, epsilon_a, epsilon_r, R, D
            )
            d_sigma = function_for_sigma(
                xi, sigma_i, N, J, alpha, beta, gamma, epsilon_a, epsilon_r, R, D
            )

            # RK4 for xi
            k1_x = dt * dx
            k2_x = dt * function_for_x(
                xi + 0.5 * k1_x,
                sigma_i,
                N,
                J,
                alpha,
                beta,
                gamma,
                epsilon_a,
                epsilon_r,
                R,
                D,
            )
            k3_x = dt * function_for_x(
                xi + 0.5 * k2_x,
                sigma_i,
                N,
                J,
                alpha,
                beta,
                gamma,
                epsilon_a,
                epsilon_r,
                R,
                D,
            )
            k4_x = dt * function_for_x(
                xi + k3_x, sigma_i, N, J, alpha, beta, gamma, epsilon_a, epsilon_r, R, D
            )
            xi = xi + (1 / 6) * (k1_x + 2 * k2_x + 2 * k3_x + k4_x)

            # RK4 for sigma_i
            k1_sigma = dt * d_sigma
            k2_sigma = dt * function_for_sigma(
                xi,
                sigma_i + 0.5 * k1_sigma,
                N,
                J,
                alpha,
                beta,
                gamma,
                epsilon_a,
                epsilon_r,
                R,
                D,
            )
            k3_sigma = dt * function_for_sigma(
                xi,
                sigma_i + 0.5 * k2_sigma,
                N,
                J,
                alpha,
                beta,
                gamma,
                epsilon_a,
                epsilon_r,
                R,
                D,
            )
            k4_sigma = dt * function_for_sigma(
                xi,
                sigma_i + k3_sigma,
                N,
                J,
                alpha,
                beta,
                gamma,
                epsilon_a,
                epsilon_r,
                R,
                D,
            )
            sigma_i = sigma_i + (1 / 6) * (
                k1_sigma + 2 * k2_sigma + 2 * k3_sigma + k4_sigma
            )
            sigma_i = torch.nn.functional.normalize(sigma_i, dim=1)

        results_xi.append(xi.clone())
        results_sigma_i.append(sigma_i.clone())

    return results_xi, results_sigma_i


# Example usage:
N = 100
J, alpha, beta, gamma, epsilon_a, epsilon_r, R = [0.1]*7
D = 3  # Ensure D is an integer
xi, sigma_i = simulate_swarmalators(N, J, alpha, beta, gamma, epsilon_a, epsilon_r, R, D)
print(xi[-1], sigma_i[-1])



import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def visualize_swarmalators(results_xi):
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(111, projection='3d')

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
