import torch
import random
import torch.nn as nn


class Swarmulator:
    def __init__(
        self,
        D=3,
        heads: int = 4,
        N=100,
        J=None,
        a=1,
        β=3,
        y=1,
        εa=None,
        εr=None,
        R=None,
    ):
        self.D = D
        self.N = N
        self.J = J if J is not None else random.uniform(-1, 1)
        self.a, self.β, self.y = a, β, y
        self.εa = εa if εa is not None else random.uniform(0, 1)
        self.εr = εr if εr is not None else random.uniform(0, 1)
        self.R = R if R is not None else random.uniform(0, 2)
        self.heads = heads

        self.xi = torch.randn(N, D)
        self.oi = torch.randn(N, D)
        self.oi /= torch.norm(self.oi, dim=1).unsqueeze(1)

        # Transformer Components
        self.attention_xi = nn.MultiheadAttention(embed_dim=D, num_heads=self.heads)
        self.attention_oi = nn.MultiheadAttention(embed_dim=D, num_heads=self.heads)

    def evolution_of_xi(self):
        attn_output, _ = self.attention_xi(self.xi, self.xi, self.xi)
        return attn_output

    def evolution_of_oi(self):
        attn_output, _ = self.attention_oi(self.oi, self.oi, self.oi)
        return attn_output

    def RK4_step(self, y, evolution_func, dt=0.01):
        k1 = dt * evolution_func()
        k2 = dt * evolution_func()
        k3 = dt * evolution_func()
        k4 = dt * evolution_func()
        return y + (k1 + 2 * k2 + 2 * k3 + k4) / 6

    def simulation(self, num_steps=1000):
        for _ in range(num_steps):
            self.xi = self.RK4_step(self.xi, self.evolution_of_xi)
            self.oi = self.RK4_step(self.oi, self.evolution_of_oi)
            # Normalizing oi to ensure it's a unit vector
            self.oi /= torch.norm(self.oi, dim=1).unsqueeze(1)
