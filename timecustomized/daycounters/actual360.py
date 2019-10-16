from timecustomized.daycounter import *


class Actual360(DayCounter):
    class Impl(DayCounter.Impl):
        def __init__(self, includeLastDay=False):
            self._includeLastDay = includeLastDay

        def name(self):
            return 'Actual/360 (inc)' if self._includeLastDay else 'Actual/360'

        def dayCount(self, d1, d2):
            return (d2 - d1).days + (1 if self._includeLastDay else 0)

        def yearFraction(self, d1, d2, refPeriodStart=None, refPeriodEnd=None):
            return ((d2 - d1).days + (1 if self._includeLastDay else 0)) / 360


    def __init__(self, includeLastDay=False):
        DayCounter.__init__(self,self.Impl(includeLastDay))
