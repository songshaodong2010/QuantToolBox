from timecustomized.daycounter import *


class Actual365(DayCounter):
    class Impl(DayCounter.Impl):
        def name(self):
            return 'Actual/365'

        def yearFraction(self, d1, d2, refPeriodStart=None, refPeriodEnd=None):
            return (d2 - d1).days / 365


    def __init__(self):
        DayCounter.__init__(self, self.Impl())
