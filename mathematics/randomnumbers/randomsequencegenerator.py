from methods.montecarlo.sample import *

class RandomSequenceGenerator:
    def __init__(self,dimensionality,rng=None,seed=0):
        if rng is not None:
            self._dimensionality = dimensionality
            self._rng = rng
            self._sequence = Sample([0]*dimensionality,1)
            self._int32Sequence=dimensionality
            if dimensionality<=0:
                raise RuntimeError('dimensionality must be greater than 0')
        else:
            self._dimensionality=dimensionality
            self._rng=seed
            self._sequence=Sample([0]*dimensionality,1)
            self._int32Sequence=dimensionality


    def nextSequence(self):
        self._sequence.weight=1
        for i in range(self._dimensionality):
            x=Sample(self._rng.next())
            self._sequence.value[i]=x.value
            self._sequence.weight*=x.weight
        return self._sequence

    def nextInt32Sequence(self):
        for i in range(self._dimensionality):
            self._int32Sequence[i]=self._rng.nextInt32()
        return self._int32Sequence

    def lastWequence(self):
        return self._sequence

    def dimension(self):
        return self._dimensionality
