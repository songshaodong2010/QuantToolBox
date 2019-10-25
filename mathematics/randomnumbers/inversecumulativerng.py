from methods.montecarlo.sample import *

class InverseCumulativeRng:
    def __init__(self,ug):
        self._uniformGenerator = ug
        self._ICND=None

    def next(self):
        sample = self._uniformGenerator.next()
        return Sample(self._ICND(sample.value),sample.weight)
