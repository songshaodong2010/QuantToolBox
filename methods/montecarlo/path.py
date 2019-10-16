import numpy as np

class Path:
    def __init__(self, timeGrid, values=None):
        self._timeGrid = timeGrid
        self._values = values
        if self._values is None:
            self._values = np.empty_like(self._timeGrid)
        if self._timeGrid.size != self._values.size:
            raise RuntimeError('different number of times and asset values')

    def empty(self):
        return self._timeGrid is None

    def length(self):
        return self._timeGrid.size

    def __getitem__(self, item):
        return self._values[item]

    def value(self,i):
        return self._values[i]

    def time(self,i):
        return self._timeGrid[i]

    def front(self):
        return self._values[0]

    def back(self):
        return self._values[-1]

    def timeGrid(self):
        return self._timeGrid
    #
    # def begin(self):
    #     return self._values.begin()
    #
    # def end(self):
    #     return self._values.end()
    #
    # def rbegin(self):
    #     return self._values.rbegin()
    #
    # def rend(self):
    #     return self._values.rend()


