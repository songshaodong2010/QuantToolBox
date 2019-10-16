from option import *
from instrument import *
from settings import *

'''
检查完毕，isExpired还需要进一步修改
'''


class OneAssetOption(Option):
    def __init__(self, payoff, exercise):
        Option.__init__(self, payoff, exercise)
        self._delta = None
        self._gamma = None
        self._vega = None
        self._theta = None
        self._rho = None

    def delta(self):
        self.calculate()
        return self._delta

    def gamma(self):
        self.calculate()
        return self._gamma

    def vega(self):
        self.calculate()
        return self._vega

    def theta(self):
        self.calculate()
        return self._theta

    def rho(self):
        self.calculate()
        return self._rho

    def fetchResults(self, r):
        if r is not None:
            Option.fetchResults(self, r)
            self._delta = r.delta
            self._gamma = r.gamma
            self._vega = r.vega
            self._theta = r.theta
            self._rho = r.rho
        else:
            raise RuntimeError('no results returned from pricing engine')

    def setupExpired(self):
        Option.setupExpired(self)
        self._delta = self._gamma = self._vega = self._theta = self._rho = 0

    def isExpired(self):  # 需要修改
        if Settings().includeReferenceDateEvents():
            return Settings().evaluationDate() < self._exercise.lastDate()
        else:
            return Settings().evaluationDate() <= self._exercise.lastDate()

    class results(Instrument.results, Option.Greeks):
        def __init__(self):
            Instrument.results.__init__(self)
            Option.Greeks.__init__(self)

        def reset(self):
            Instrument.results.reset(self)
            Option.Greeks.reset(self)

    class engine(GenericEngine):
        def __init__(self):
            GenericEngine.__init__(self)
            self._results = OneAssetOption.results()
            self._arguments = Option.arguments()
