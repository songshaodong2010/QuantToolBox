from termstructures.volatility.equityfx.blackvoltermstructure import *
from timecustomized.daycounters.actual360 import *
from quotes.simplequote import *

'''
检查完毕，无需修改
'''


class BlackConstantVol(BlackVolatilityTermStructure):
    def __init__(self, volatility, dc, cal, bdc=BusinessDayConvention.Following, referenceDate=None,
                 settlementDays=None):
        if referenceDate is not None and settlementDays is None:
            BlackVolTermStructure.__init__(self, bdc, referenceDate=referenceDate, cal=cal, dc=dc)
            if isinstance(volatility, Handle):
                self._volatility = volatility
                self.registerWith(self._volatility)
            else:
                self._volatility = SimpleQuote(volatility)
        elif settlementDays is not None and referenceDate is None:
            BlackVolTermStructure.__init__(self, bdc, settlementDays=settlementDays, cal=cal, dc=dc)
            if isinstance(volatility, Handle):
                self._volatility = volatility
                self.registerWith(self._volatility)
            else:
                self._volatility = SimpleQuote(volatility)
        else:
            raise RuntimeError('Wrong Parameter!')

    def maxDate(self):
        return datetime.date(2099, 12, 31)

    def minStrike(self):
        return -999999999

    def maxStrike(self):
        return 999999999

    def blackVolImpl(self, t, strike):
        return self._volatility.value()
