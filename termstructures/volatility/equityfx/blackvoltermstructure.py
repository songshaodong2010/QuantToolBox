from termstructures.voltermstructure import *
from timecustomized.businessdayconvention import *
import numpy as np

'''
检查完毕，无需修改
'''


class BlackVolTermStructure(VolatilityTermStructure):
    def __init__(self, bdc=BusinessDayConvention.Following, dc=None, referenceDate=None, cal=None, settlementDays=None):
        if referenceDate is None and settlementDays is None:
            VolatilityTermStructure.__init__(self, bdc, dc=dc)
        elif referenceDate is not None and settlementDays is None:
            VolatilityTermStructure.__init__(self, bdc, referenceDate=referenceDate, cal=cal, dc=dc)
        elif settlementDays is not None and referenceDate is None:
            VolatilityTermStructure.__init__(self, bdc, settlementDays=settlementDays, cal=cal, dc=dc)
        else:
            raise RuntimeError('Wrong Parameter!')

    def blackVol(self, maturity, strike, extrapolate=False):
        self.checkRange(maturity, extrapolate)
        self.checkStrike(strike, extrapolate)
        if isinstance(maturity, datetime.date):
            t = self.timeFromReference(maturity)
            return self.blackVolImpl(t, strike)
        else:
            return self.blackVolImpl(maturity, strike)

    def blackVariance(self, maturity, strike, extrapolate=False):
        self.checkRange(maturity, extrapolate)
        self.checkStrike(strike, extrapolate)
        if isinstance(maturity, datetime.date):
            t = self.timeFromReference(maturity)
            return self.blackVarianceImpl(t, strike)
        else:
            return self.blackVarianceImpl(maturity, strike)

    def blackForwardVol(self, time1, time2, strike, extrapolate=False):
        if isinstance(time1, datetime.date) and isinstance(time2, datetime.date):
            if time1 > time2:
                raise RuntimeError('date1 later than date2')
            self.checkRange(time2, extrapolate)
            t1 = self.timeFromReference(time1)
            t2 = self.timeFromReference(time2)
        else:
            t1 = time1
            t2 = time2
        if t1 > t2:
            raise RuntimeError('time1 later than  time2')
        self.checkRange(t2, extrapolate)
        self.checkStrike(strike, extrapolate)
        if t1 == t2:
            if t1 == 0:
                epsilon = 10 ^ -5
                var = self.blackVarianceImpl(epsilon, strike)
                return np.sqrt(var / epsilon)
            else:
                epsilon = min(10 ^ -5, time1)
                var1 = self.blackVarianceImpl(time1 - epsilon, strike)
                var2 = self.blackVarianceImpl(time1 + epsilon, strike)
                if var1 < var2:
                    raise RuntimeError('variances must be non-decreasing')
                return np.sqrt((var2 - var1) / (2 * epsilon))
        else:
            var1 = self.blackVarianceImpl(t1, strike)
            var2 = self.blackVarianceImpl(t2, strike)
            if var1 < var2:
                raise RuntimeError('variances must be non-decreasing')
            return np.sqrt((var2 - var1) / (t2 - t1))

    def blackForwardVarience(self, time1, time2, strike, extrapolate=False):
        if isinstance(time1, datetime.date) and isinstance(time2, datetime.date):
            if time1 > time2:
                raise RuntimeError('date1 later than date2')
            self.checkRange(time2, extrapolate)
            t1 = self.timeFromReference(time1)
            t2 = self.timeFromReference(time2)
        else:
            t1 = time1
            t2 = time2
        if t1 > t2:
            raise RuntimeError('time1 later than  time2')
        self.checkRange(t2, extrapolate)
        self.checkStrike(strike, extrapolate)
        var1 = self.blackVarianceImpl(time1, strike)
        var2 = self.blackVarianceImpl(time2, strike)
        if var1 < var2:
            raise RuntimeError('variances must be non-decreasing')
        return var2 - var1

    def blackVarianceImpl(self, t, strike):
        pass

    def blackVolImpl(self, t, strike):
        pass


class BlackVolatilityTermStructure(BlackVolTermStructure):
    def __init__(self, bdc=BusinessDayConvention.Following, dc=None, referenceDate=None, cal=None, settlementDays=None):
        if referenceDate is None and settlementDays is None:
            BlackVolTermStructure.__init__(self, bdc, dc=dc)
        elif referenceDate is not None and settlementDays is None:
            BlackVolTermStructure.__init__(self, bdc, referenceDate=referenceDate, cal=cal, dc=dc)
        elif settlementDays is not None and referenceDate is None:
            BlackVolTermStructure.__init__(self, bdc, settlementDays=settlementDays, cal=cal, dc=dc)
        else:
            raise RuntimeError('Wrong Parameter!')

    def blackVarianceImpl(self, t, strike):
        vol = self.blackVolImpl(t, strike)
        return vol * vol * t


class BlackVarianceTermStructure(BlackVolTermStructure):
    def __init__(self, bdc=BusinessDayConvention.Following, dc=None, referenceDate=None, cal=None, settlementDays=None):
        if referenceDate is None and settlementDays is None:
            BlackVolTermStructure.__init__(self, bdc, dc=dc)
        elif referenceDate is not None and cal is None and settlementDays is None:
            BlackVolTermStructure.__init__(self, bdc, referenceDate=referenceDate, cal=cal, dc=dc)
        elif settlementDays is not None and cal is not None and dc is not None and referenceDate is None:
            BlackVolTermStructure.__init__(self, bdc, settlementDays=settlementDays, cal=cal, dc=dc)
        else:
            raise RuntimeError('Wrong Parameter!')

    def blackVolImpl(self, t, strike):
        nonZeroMaturity = 10 ^ -5 if t == 0 else t
        var = self.blackVarianceImpl(nonZeroMaturity, strike)
        return np.sqrt(var / nonZeroMaturity)
