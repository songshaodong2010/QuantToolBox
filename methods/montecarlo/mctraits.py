from methods.montecarlo.pathgenerator import *
from methods.montecarlo.multipathgenerator import *
from methods.montecarlo.pathpricer import *
from mathematics.randomnumbers.rngtraits import *

class SingleVariate:
    def __init__(self):
        self.rng_traits = PseudoRandom
        self.path_type = Path
        self.path_pricer_type = PathPricer
        self.rsg_type = self.rng_traits.rsg_type
        self.path_generator_type = PathGenerator
        self.allowsErrorEstimate = self.rng_traits.allowsErrorEstimate



class MultiVariate:
    def __init__(self):
        self.rng_traits = PseudoRandom
        self.path_type = Path
        self.path_pricer_type = PathPricer
        self.rsg_type = self.rng_traits.rsg_type
        self.path_generator_type = MultiPathGenerator
        self.allowsErrorEstimate = self.rng_traits.allowsErrorEstimate
