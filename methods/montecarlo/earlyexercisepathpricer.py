from methods.montecarlo.path import *
from methods.montecarlo.multipath import *


class EarlyExerciseTraits:
    def pathLength(self, path):
        if isinstance(path, Path):
            return path.length()
        elif isinstance(path, MultiPath):
            return path.pathSize()
        else:
            raise RuntimeError('Wrong Path Type!')


class EarlyExercisePathPricer:
    def __call__(self,path,t):
        pass

    def state(self,path,t):
        pass

    def basisSystem(self):
        pass
    