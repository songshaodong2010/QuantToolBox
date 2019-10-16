from stochasticprocess import *
import numpy as np


class EulerDiscretization(StochasticProcess.discretization,StochasticProcess1D.discretization):
    def drift(self, process, t0, x0, dt):
        return process.drift(t0, x0) * dt

    def diffusion(self, process, t0, x0, dt):
        return process.diffusion(t0, x0) * np.sqrt(dt)

    def variance(self, process, t0, x0, dt):
        sigma = process.diffusion(t0, x0)
        return sigma * sigma * dt
