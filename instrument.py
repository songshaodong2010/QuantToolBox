from patterns.lazyobject import *
from pricingengine import *

'''
检查完毕，无需修改
'''


class Instrument(LazyObject):
    def __init__(self):
        LazyObject.__init__(self)
        self._NPV = None
        self._errorEstimate = None
        self._valuationDate = None
        self._engine = None

    def NPV(self):
        self.calculate()
        if self._NPV is None:
            raise RuntimeError('NPV not provided')
        return self._NPV

    def errorEstimate(self):
        self.calculate()
        if self._errorEstimate is None:
            raise RuntimeError('error estimate not provided')
        return self._errorEstimate

    def valuationDate(self):
        self.calculate()
        if self._valuationDate is None:
            raise RuntimeError('valuation date not provided')
        return self._valuationDate

    def isExpired(self):
        pass

    def setPricingEngine(self, e):
        if self._engine is not None:
            self.unregisterWith(self._engine)
        self._engine = e
        if self._engine is not None:
            self.registerWith(e)
        self.update()

    def setupArguments(self, argument):
        pass

    def fetchResults(self, r):
        if r is not None:
            self._NPV = r.value
            self._errorEstimate = r.errorEstimate
            self._valuationDate = r.valuationDate
        else:
            raise RuntimeError('no results returned from pricing engine')

    def calculate(self):
        if not self._calculated:
            if self.isExpired():
                self.setupExpired()
                self._calculated = True
            else:
                LazyObject.calculate(self)

    def setupExpired(self):
        self._NPV = 0.0
        self._errorEstimate = 0.0
        self._valuationDate = None

    def performCalculations(self):
        if self._engine is not None:
            self._engine.reset()
            self.setupArguments(self._engine.getArguments())
            self._engine.getArguments().validate()
            self._engine.calculate()
            self.fetchResults(self._engine.getResults())
        else:
            raise RuntimeError('null pricing engine')

    class results(PricingEngine.results):
        def __init__(self):
            self.value = None
            self.errorEstimate = None
            self.valuationDate = None

        def reset(self):
            self.valuationDate = None
            self.value = None
            self.errorEstimate = None
