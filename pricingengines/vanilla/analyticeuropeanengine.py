from instruments.vanillaoption import *
from instruments.payoffs import *
from exercise import *
from pricingengines.blackcalculator import *
import numpy as np


class AnalyticEuropeanEngine(VanillaOption.engine):
    def __init__(self, process, discountCurve=None):
        super().__init__()
        self._process = process
        self.registerWith(self._process)
        self._discountCurve = discountCurve
        if self._discountCurve is not None:
            self.registerWith(self._discountCurve)

    def calculate(self):
        if not isinstance(self._arguments.exercise,EuropeanExercise):
            raise RuntimeError('not an European option')
        if not isinstance(self._arguments.payoff,StrikedTypePayoff):
            raise RuntimeError('non-striked payoff given')
        if  self._discountCurve is None:
            discountPtr = self._process.riskFreeRate()
            # discountPtr = self._process.riskFreeRate().currentLink()
        else:
            discountPtr = self._discountCurve
            # discountPtr = self._discountCurve.currentLink()
        variance = self._process.blackVolatility().blackVariance(self._arguments.exercise.lastDate(),
                                                                 self._arguments.payoff.strike())
        dividendDiscount = self._process.dividendYield().discount(self._arguments.exercise.lastDate())
        df = discountPtr.discount(self._arguments.exercise.lastDate())
        riskFreeDiscountForFwdEstimation = self._process.riskFreeRate().discount(self._arguments.exercise.lastDate())
        spot = self._process.stateVariable().value()
        if spot <= 0:
            raise RuntimeError('negative or null underlying given')
        forwardPrice = spot * dividendDiscount / riskFreeDiscountForFwdEstimation
        black = BlackCalculator(self._arguments.payoff, forwardPrice, np.sqrt(variance), df)
        self._results.value = black.value()
        self._results.delta = black.delta(spot)
        self._results.gamma = black.gamma(spot)
        rfdc = discountPtr.dayCounter()
        voldc = self._process.blackVolatility().dayCounter()
        t = rfdc.yearFraction(self._process.riskFreeRate().referenceDate(), self._arguments.exercise.lastDate())
        self._results.rho = black.rho(t)
        t = voldc.yearFraction(self._process.blackVolatility().referenceDate(), self._arguments.exercise.lastDate())
        self._results.vega = black.vega(t)
        try:
            self._results.theta = black.theta(spot,t)
        except:
            self._results.theta = None