from methods.montecarlo.multipath import MultiPath
from methods.montecarlo.sample import Sample
from stochasticprocess import *
import numpy as np


class MultiPathGenerator:
    def __init__(self, process, times, generator, brownianBridge=False):
        self._brownianBridge = brownianBridge
        self._process = process
        self._generator = generator
        self._next = Sample(MultiPath(nAsset=self._process.size(), timeGrid=times), 1)
        if self._generator.dimension() != self._process.factors() * (times.size() - 1):
            raise RuntimeError('dimension is not equal to the number of factors times the number of time steps')
        if times.size() <= 1:
            raise RuntimeError('no times given')

    def next(self, antithetic=None):
        if antithetic is None:
            return self.next(antithetic=False)
        else:
            if self._brownianBridge:
                raise RuntimeError('Brownian bridge not supported')
            else:
                sequence = self._generator.lastSequence() if antithetic else self._generator.nextSequence()
            m = self._process.size()
            n = self._process.factors()
            path = self._next.value
            asset = self._process.initialValues()
            for j in range(m):
                path[j]._values[0] = asset[j]
            self._next.weight = sequence.weight
            timeGrid = path[0].timeGrid()
            for i in range(1, path.pathSize):
                offset = (i - 1) * n
                t = timeGrid[i - 1]
                dt = timeGrid.dt(i - 1)
                if antithetic:
                    temp = [-item for item in sequence[offset:offset + n]]
                else:
                    temp = sequence[offset:offset + n]
                asset = self._process.evolve(t, asset, dt, temp)
                for j in range(m):
                    path[j][i] = asset[j]
        return self._next

    def antithetic(self):
        return self.next(antithetic=True)
