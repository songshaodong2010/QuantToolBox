from methods.montecarlo.multipath import MultiPath
from methods.montecarlo.sample import Sample
from stochasticprocess import *
import numpy as np

class MultiPathGenerator:
    def __init__(self,process,times,generator,brownisnBridge=False):
        self._brownianBridge = brownisnBridge
        self._process = process
        self._generator = generator
        self._next = (MultiPath(self._process.size(),times),1)

    def next(self,antithetic=None):
        if antithetic is None:
            return self.next(antithetic=False)
        else:
            if self._brownianBridge:
                raise RuntimeError('Brownian bridge not supported')
            else:
                sequence = self._generator.lastSequence() if antithetic else self._generator.nextSequence()
            m=self._process.size()
            n=self._process.factors()
            path = self._next.value
            asset = self.process.initialValues()
            for j in range(m):
                path[j].front()=asset[j]
            temp = []
            self._next.weight = sequence.weight
            timeGrid = path[0].timeGrid()
            for i in range(1,path.pathSize):
                offset = (i-1)*n
                t=timeGrid[i-1]
                dt = timeGrid.dt(i-1)
                if antithetic:
                    tranform(sequence.value.begin()+offset,sequence.value.begin()+offset+n,self.temp.begin(),None)
                else:
                    copy(sequence.value.begin()+offset,sequence.value.begin()+offset+n,self.temp.begin())
            asset = self._process.evolve(t,asset,dt,temp)
            for j in range(m):
                path[j][i]=asset[j]
        return self._next


    def antithetic(self):
        return self.next(antithetic=True)