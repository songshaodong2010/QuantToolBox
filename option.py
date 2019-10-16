from instrument import *
from enum import Enum

'''
检查完毕，无需修改
'''


class Option(Instrument):
    class Type(Enum):
        Call = 1
        Put = -1

    def __init__(self, payoff, exercise):
        Instrument.__init__(self)
        self._payoff = payoff
        self._exercise = exercise

    def payoff(self):
        return self._payoff

    def exercise(self):
        return self._exercise

    class arguments(PricingEngine.arguments):
        def __init__(self):
            self.payoff = None
            self.exercise = None

        def validate(self):
            if self.payoff is None:
                raise RuntimeError('no payoff given')
            if self.exercise is None:
                raise RuntimeError('no exercise given')

    class Greeks(PricingEngine.results):
        def __init__(self):
            self.delta = None
            self.gamma = None
            self.theta = None
            self.vega = None
            self.rho = None

        def reset(self):
            self.delta = None
            self.gamma = None
            self.theta = None
            self.vega = None
            self.rho = None

    def setupArguments(self, args):
        if args is None:
            raise RuntimeError('wrong argument type')
        args.payoff = self._payoff
        args.exercise = self._exercise
