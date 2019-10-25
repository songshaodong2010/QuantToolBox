from methods.montecarlo.pathgenerator import *
from mathematics.randomnumbers.randomsequencegenerator import *
from mathematics.randomnumbers.inversecumulativersg import *


class GenericPseudoRandom:
    def __init__(self,urng_type,ic_type):
        self.allowErrorEstimate = 1
        self.icInstance = None
        self.urng_type=urng_type
        self.ic_type=ic_type

    def make_sequence_generator(self, dimension, seed):
        g = RandomSequenceGenerator(dimension, seed=seed)
        return InverseCumulativeRsg(g, self.urng_type,self.ic_type,inverseCum=self.icInstance) if self.icInstance else InverseCumulativeRsg(g)

class PseudoRandom(GenericPseudoRandom):
    URNG=MersenneTwisterUniformRng
    IC=InverseCumulativeNormal

class GenericLowDiscrepancy:
    def __init__(self):
        self.ursg = None
        self.rsg = None
        self.allowErrorEstimate = None
        self.icInstance = None

    def make_sequence_generator(self, dimension, seed):
        g = RandomSequenceGenerator(dimension, seed=seed)
        return InverseCumulativeRsg(g, inverseCum=self.icInstance) if self.icInstance else InverseCumulativeRsg(g)