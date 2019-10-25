from methods.montecarlo.path import Path
from methods.montecarlo.sample import Sample
import numpy as np


class BrownianBridge:
    def __init__(self, steps=None, times=None, timeGrid=None):
        if steps is not None and times is None and timeGrid is None:
            self._size = steps
            self._t = [0] * self._size
            self._sqrtdt = [0] * self._size
            self._bridgeIndex = [0] * self._size
            self._leftIndex = [0] * self._size
            self._rightIndex = [0] * self._size
            self._leftWeight = [0] * self._size
            self._rightWeight = [0] * self._size
            self._stdDev = [0] * self._size
            for i in range(self._size):
                self._t[i] = i + 1
            self.initialize()
        if steps is None and times is not None and timeGrid is None:
            self._size = times.size()
            self._t = times
            self._sqrtdt = [0] * self._size
            self._bridgeIndex = [0] * self._size
            self._leftIndex = [0] * self._size
            self._rightIndex = [0] * self._size
            self._leftWeight = [0] * self._size
            self._rightWeight = [0] * self._size
            self._stdDev = [0] * self._size
            self.initialize()
        if steps is None and times is None and timeGrid is not None:
            self._size = timeGrid.size() - 1
            self._t = [0] * self._size
            self._sqrtdt = [0] * self._size
            self._bridgeIndex = [0] * self._size
            self._leftIndex = [0] * self._size
            self._rightIndex = [0] * self._size
            self._leftWeight = [0] * self._size
            self._rightWeight = [0] * self._size
            self._stdDev = [0] * self._size
            for i in range(self._size):
                self._t[i] = timeGrid[i + 1]

    def initialize(self):
        self._sqrtdt[0] = np.sqrt(self._t[0])
        for i in range(1, self._size):
            self._sqrtdt[i] = np.sqrt(self._t[i] - self._t[i - 1])
        map = [0]*self._size
        map[-1] = 1
        self._bridgeIndex[0] = self._size - 1
        self._stdDev[0] = np.sqrt(self._t[self._size - 1])
        self._leftWeight[0] = self._rightWeight[0] = 0
        j = 0
        for i in range(1, self._size):
            while (map[j]):
                j = j + 1
            k = j
            while (not map[k]):
                k = k + 1
            l = j + ((k - 1 - j) >> 1)
            map[l] = i
            self._bridgeIndex[i] = l
            self._leftIndex[i] = j
            self._rightIndex[i] = k
            if j != 0:
                self._leftWeight[i] = (self._t[k] - self._t[l]) / (self._t[k] - self._t[j - 1])
                self._rightWeight[i] = (self._t[l] - self._t[j - 1]) / (self._t[k] - self._t[j - 1])
                self._stdDev[i] = np.sqrt(
                    (self._t[l] - self._t[j - 1]) * (self._t[k] - self._t[l]) / (self._t[k] - self._t[j - 1]))
            else:
                self._leftWeight[i] = (self._t[k] - self._t[l]) / self._t[k]
                self._rightWeight[i] = self._t[l] / self._t[k]
                self._stdDev[i] = np.sqrt(self._t[l] * (self._t[k] - self._t[l]) / self._t[k])
            j = k + 1
            if j >= self._size:
                j = 0

    def size(self):
        return self._size

    def times(self):
        return self._t

    def bridgeIndex(self):
        return self._bridgeIndex

    def leftIndex(self):
        return self._leftIndex

    def rightIndex(self):
        return self._rightIndex

    def leftWeight(self):
        return self._leftWeight

    def rightWeight(self):
        return self._rightWeight

    def stdDeviation(self):
        return self._stdDev

    def transform(self, sequence, output):
        if len(sequence) == 0:
            raise RuntimeError('invalid sequence')
        if len(sequence) != self._size:
            raise RuntimeError('incompatible sequence size')
        output[self._size - 1] = self._stdDev[0] * sequence[0]
        for i in range(1, self._size):
            j = self._leftIndex[i]
            k = self._rightIndex[i]
            l = self._bridgeIndex[i]
            if j != 0:
                output[l] = self._leftWeight[i] * output[j - 1] + self._rightWeight[i] * output[k] + self._stdDev[i] * \
                            sequence[i]
            else:
                output[l] = self._rightWeight[i] * output[k] + self._stdDev[i] * sequence[i]
        for i in range(self._size-1, 0, -1):
            output[i] -= output[i - 1]
            output[i] /= self._sqrtdt[i]
        output[0] /= self._sqrtdt[0]
