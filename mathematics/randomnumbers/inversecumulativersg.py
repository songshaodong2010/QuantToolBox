from methods.montecarlo.sample import *

class InverseCumulativeRsg:
    def __init__(self,usg,usg_type,ic_type,inverseCum=None):
        self._uniformSequenceGenerator = usg
        self._dimension = self._uniformSequenceGenerator.dimesion()
        self._x = [1] * self._dimension
        self.usg_type=usg_type
        self.ic_type=ic_type
        if inverseCum is not None:
            self._ICD=inverseCum

    def nextSequence(self):
        sample=self._uniformSequenceGenerator.nextSequence()
        self._x.weight=sample.weight
        for i in range(self._dimension):
            self._x.weight[i] = self._ICD(sample.value[i])
        return self._x



