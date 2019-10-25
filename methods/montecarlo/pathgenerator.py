from timegrid import *
from methods.montecarlo.sample import *
from methods.montecarlo.path import *


class PathGenerator:
    def __init__(self, process, generator, brownianBridge, length=None, timeSteps=None, timeGrid=None):
        if length is not None and timeSteps is not None and timeGrid is None:
            self._brownianBridge = brownianBridge
            self._generator = generator
            self._dimension = self._generator.dimension()
            self._timeGrid = TimeGrid(end=length, steps=timeSteps)
            self._process = process
            self._next = Sample(Path(self._timeGrid), 1)
            self._temp = self._dimension
            self._bb = self._timeGrid
            if self._dimension != timeSteps:
                raise RuntimeError('sequence generator dimensionality != timeSteps')
        elif length is None and timeSteps is None and timeGrid is not None:
            self._brownianBridge = brownianBridge
            self._generator = generator
            self._dimension = self._generator.demension()
            self._timeGrid = timeGrid
            self._process = process
            self._next = Sample(Path(self._timeGrid), 1)
            self._temp = self._dimension
            self._bb = self._timeGrid
            if self._dimension != self._timeGrid.size()-1:
                raise RuntimeError('sequence generator dimensionality != timeSteps')
        else:
            raise RuntimeError('Wrong parameter!')

    def next(self, antithetic=None):
        if antithetic is None:
            return self.next(antithetic=False)
        else:
            sequence = self._generator.lastSequence() if antithetic else self._generator.nextSequence()
            if self._brownianBridge:
                self._bb.tranform(sequence.value.begin(), sequence.value.end(), self._temp.begin())
            else:
                self._temp = sequence.value
            self._next.weight = sequence.weight
            path = self._next.value
            path._values[0] = self._process.x0()
            for i in range(1,path.length()):
                t=self._timeGrid[i-1]
                dt = self._timeGrid.dt(i-1)
                path[i]=self._process.evolve(t,path[i-1],dt,-self._temp[i-1] if antithetic else self._temp[i-1])
            return self._next

    def antithetic(self):
        return self.next(antithetic=True)

    def size(self):
        return self._dimension

    def timeGrid(self):
        return self._timeGrid
