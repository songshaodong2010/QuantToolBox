from stochasticprocess import *
from processes.eulerdiscretization import EulerDiscretization
from compounding import Compounding
from timecustomized.frequency import Frequency
from termstructures.yields.flatforward import FlatForward
from timecustomized.daycounters.actual365 import Actual365
from timecustomized.calendars.nullcalendar import NullCalendar


class GeneralizedBlackScholesProcess(StochasticProcess1D):
    def __init__(self, x0, dividendTS, riskFreeTS, blackVolTS, localVolTS=None, disc=EulerDiscretization(),
                 forceDiscretization=False):
        StochasticProcess1D.__init__(self, disc=disc)
        if localVolTS is not None:
            self._x0 = x0
            self._dividendYield = dividendTS
            self._riskFreeRate = riskFreeTS
            self._blackVolatility = blackVolTS
            self._externalLocalVolTS = localVolTS
            self._forceDiscretization = False
            self._hasExternalVol = True
            self._updated = False
            self._localVolatility = None
            self._isStrikeIndependent = False
            self.registerWith(self._x0)
            self.registerWith(self._riskFreeRate)
            self.registerWith(self._dividendYield)
            self.registerWith(self._blackVolatility)
            self.registerWith(self._externalLocalVolTS)
        else:
            self._x0 = x0
            self._dividendYield = dividendTS
            self._riskFreeRate = riskFreeTS
            self._blackVolatility = blackVolTS
            self._forceDiscretization = forceDiscretization
            self._hasExternalVol = False
            self._updated = False
            self._localVolatility = None
            self._isStrikeIndependent = False
            self.registerWith(self._x0)
            self.registerWith(self._riskFreeRate)
            self.registerWith(self._dividendYield)
            self.registerWith(self._blackVolatility)

    # 现在还不知道x0的类型
    def x0(self):
        return self._x0.value()

    def drift(self, t, x):
        sigma = self.diffusion(t, x)
        t1 = t + 0.0001
        return self._riskFreeRate.forwardRate(Compounding.Continuous, Frequency.NoFrequency, t1=t, t2=t1,
                                              extrapolate=True) \
               - self._dividendYield.forwardRate(Compounding.Continuous, Frequency.NoFrequency, t1=t, t2=t1,
                                                 extrapolate=True) \
               - 0.5 * sigma * sigma

    def diffusion(self, t, x):
        return self.localVolatility().localVol(t, x, True)

    def apply(self, x0, dx):
        return x0 * np.exp(dx)

    def expectation(self, t0, x0, dt):
        self.localVolatility()
        if self._isStrikeIndependent and (not self._forceDiscretization):
            return x0 * np.exp(
                dt * (self._riskFreeRate.forwardRate(Compounding.Continuous, Frequency.NoFrequency, t1=t0, t2=t0 + dt,
                                                     extrapolate=True) - self._dividendYield.forwardRare(
                    Compounding.Continuous, Frequency.NoFrequency, t1=t0, t2=t0 + dt,
                    extrapolate=True)))
        else:
            raise RuntimeError('not implemented')

    def stdDeviation(self, t0, x0, dt):
        self.localVolatility()
        if self._isStrikeIndependent and (not self._forceDiscretization):
            return np.sqrt(self.variance(t0, x0, dt))
        else:
            return self._discretization.diffusion(self, t0, x0, dt)

    def variance(self, t0, x0, dt):
        self.localVolatility()
        if self._isStrikeIndependent and (not self._forceDiscretization):
            return self._blackVolatility.blackVariance(t0 + dt, 0.01) - self._blackVolatility.blackVariance(t0, 0.01)
        else:
            self._discretization.variance(self, t0, x0, dt)

    def evolve(self, t0, x0, dt, dw):
        self.localVolatility()
        if self._isStrikeIndependent and (not self._forceDiscretization):
            var = self.variance(t0, x0, dt)
            drift = (self._riskFreeRate.forwardRate(Compounding.Continuous, Frequency.NoFrequency, t1=t0, t2=t0 + dt,
                                                    extrapolate=True)
                     - self._dividendYield.forwardRare(Compounding.Continuous, Frequency.NoFrequency, t1=t0, t2=t0 + dt,
                                                       extrapolate=True)) * dt - 0.5 * var
            return self.apply(x0, np.sqrt(var) * dw + drift)
        else:
            return self.apply(x0, self._discretization.drift(self, t0, x0, dt) + self.stdDeviation(t0, x0, dt) * dw)

    def time(self, d):
        return self._riskFreeRate.daycounter().yearFraction(self._riskFreeRate.referenceDate(), d)

    def update(self):
        self.__updated = False
        StochasticProcess1D.update(self)

    def stateVariable(self):
        return self._x0

    def dividendYield(self):
        return self._dividendYield

    def riskFreeRate(self):
        return self._riskFreeRate

    def blackVolatility(self):
        return self._blackVolatility

    # 有待完善
    def localVolatility(self):
        return self._localVolatility


class BlackscholesProcess(GeneralizedBlackScholesProcess):
    def __init__(self, x0, riskFreeTS, blackVolTS, d=EulerDiscretization(), forceDiscretization=False):
        GeneralizedBlackScholesProcess.__init__(self, x0,
                                                FlatForward(0, Actual365(), cal=NullCalendar(), settlementDays=0),
                                                riskFreeTS,
                                                blackVolTS, disc=d,
                                                forceDiscretization=forceDiscretization)


class BlackscholesMertonProcess(GeneralizedBlackScholesProcess):
    def __init__(self, x0, dividendTS, riskFreeTS, blackVolTS, d=EulerDiscretization(), forceDiscretization=False):
        GeneralizedBlackScholesProcess.__init__(self, x0, dividendTS, riskFreeTS, blackVolTS, disc=d,
                                                forceDiscretization=forceDiscretization)


class BlackProcess(GeneralizedBlackScholesProcess):
    def __init__(self, x0, riskFreeTS, blackVolTS, d=EulerDiscretization(), forceDiscretization=False):
        GeneralizedBlackScholesProcess.__init__(self, x0, riskFreeTS, riskFreeTS, blackVolTS, disc=d,
                                                forceDiscretization=forceDiscretization)
