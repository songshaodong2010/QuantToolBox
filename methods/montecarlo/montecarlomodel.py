from methods.montecarlo.mctraits import *


class MonteCarloModel:
    def __init__(self, pathGenerator, pathPricer, randomNumberGenerator, sampleAccumulator, antitheticVariate,
                 cvPathPricer=None, cvOptionValue=None, cvPathGenerator=None):
        self._pathGenerator = pathGenerator
        self._pathPricer = pathPricer
        self._randomNumberGenerator = randomNumberGenerator
        self._sampleAccumulator = sampleAccumulator
        self._isAntitheticVariate = antitheticVariate
        self._cvPathPricer = cvPathPricer
        self._cvOptionValue = cvOptionValue
        self._cvPathGenerator = cvPathGenerator
        if self._cvPathPricer is None:
            self._isControlVariate = True
        else:
            self._isControlVariate = False

    def addSamples(self, samples):
        for j in range(1, samples + 1):
            path = self._pathGenerator.next()
            price = self._pathPricer(path.value)
            if self._isControlVariate:
                if self._cvPathGenerator is not None:
                    price = price + self._cvOptionValue - self._cvPathPricer(path.value)
                else:
                    cvPath = self._cvPathGenerator.next()
                    price = price + self._cvOptionValue - self._cvPathPricer(cvPath.value)
            if self._isAntitheticVariate:
                atPath = self._pathGenerator.antithetic()
                price2 = self._pathPricer(atPath.value)
                if self._isControlVariate:
                    if self._cvPathGenerator is not None:
                        price2 = price2 + self._cvOptionValue - self._cvPathPricer(atPath.value)
                    else:
                        cvPath = self._cvPathGenerator.antithetic()
                        price2 = price2 + self._cvOptionValue - self._cvPathPricer(cvPath.value)
                self._sampleAccumulator.add((price + price2) / 2, path.weight)
            else:
                self._sampleAccumulator.add(price, path.weight)

    def sampleAccumulator(self):
        return self._sampleAccumulator
