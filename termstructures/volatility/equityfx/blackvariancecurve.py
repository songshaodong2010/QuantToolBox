from termstructures.volatility.equityfx.blackvoltermstructure import *
from mathematics.interpolation import *


class BlackVarianceCurve(BlackVolatilityTermStructure):
    def __init__(self, referenceDate, dates, blackVolCurve, dayCounter, forceMonotoneVariance=True):
        BlackVolatilityTermStructure.__init__(self, referenceDate)
        self._dayCounter = dayCounter
        self._maxDate = dates[-1]
        self._varianceCurve=None
        if len(dates) != blackVolCurve.size():
            raise RuntimeError('mismatch between date vector and black vol vector')
        if dates[0] <= referenceDate:
            raise RuntimeError('cannot have dates[0] <= referenceDate')
        self._variance = [0] * (len(dates) + 1)
        self._times = [0] * (len(dates) + 1)
        for j in range(1, blackVolCurve.size() + 1):
            self._times[j] = self.timeFromReference(dates[j - 1])
            if self._times[j] <= self._times[j - 1]:
                raise RuntimeError('dates must be sorted unique!')
            self._variance[j] = self._times[j] * blackVolCurve[j - 1] * blackVolCurve[j - 1]
            if self._variance[j] < self._variance[j - 1]:
                raise RuntimeError('variance must be non-decreasing')
        self.setInterpolation()

    def dayCounter(self):
        return self._dayCounter

    def minStrike(self):
        return -999999999

    def maxStrike(self):
        return 999999999

    def setInterpolation(self, i=Interpolator()):
        self._varianceCurve = i.interpolate(self._times[0], self._times[-1], self._variance[0])
        self._varianceCurve.update()
        self.notifyObservers()

    def blackVarianceImpl(self, t, strike):
        if t<self._times[-1]:
            return self._varianceCurve(t,True)
        else:
            return self._varianceCurve(self._times[-1],True)*t/self._times[-1]

    def maxDate(self):
        return self._maxDate
