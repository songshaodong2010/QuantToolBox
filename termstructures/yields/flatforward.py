from patterns.lazyobject import *
from termstructures.yieldtermstructure import *
from quotes.simplequote import *
from compounding import *
from timecustomized.frequency import *

'''
检查完毕，无需修改
'''

class FlatForward(YieldTermStructure, LazyObject):
    def __init__(self, forward, dayCounter, compounding=Compounding.Continuous, frequency=Frequency.Annual, referenceDate=None, settlementDays=None,
                 cal=None):
        LazyObject.__init__(self)
        if referenceDate is not None and settlementDays is None and cal is not None:
            YieldTermStructure.__init__(self, dayCounter, referenceDate=referenceDate,cal=cal)
            if isinstance(forward, Handle):
                self._forward = forward
                self.registerWith(self._forward)
            else:
                self._forward = SimpleQuote(forward)
            self._compounding = compounding
            self._frequency = frequency
        elif referenceDate is None and settlementDays is not None and cal is not None:
            YieldTermStructure.__init__(self, dayCounter,settlementDays=settlementDays, cal=cal)
            if isinstance(forward, Quote):
                self._forward = forward
                self.registerWith(self._forward)
            else:
                self._forward = SimpleQuote(forward)
            self._compounding = compounding
            self._frequency = frequency

    def compounding(self):
        return self._compounding

    def compoundingFrequency(self):
        return self._frequency

    def maxDate(self):
        return datetime.date(2099,12,31)

    def update(self):
        LazyObject.update(self)
        YieldTermStructure.update(self)

    def performCalculations(self):
        self._rate = InterestRate(self._forward.value(), self.dayCounter(), self._compounding, self._frequency)

    def discountImpl(self, t):
        self.calculate()
        return self._rate.discountFactor(t)
