from termstructure import *

class VolatilityTermStructure(TermStructure):
    def __init__(self,bdc,dc=None,referenceDate=None,cal=None,settlementDays=None):
        if referenceDate is None and cal is None and settlementDays is None:
            TermStructure.__init__(self,dc=dc)
            self._bdc=bdc
        elif referenceDate is not None and cal is not None and settlementDays is None:
            TermStructure.__init__(self, referenceDate=referenceDate,cal=cal,dc=dc)
            self._bdc = bdc
        elif settlementDays is not None and cal is not None and dc is not None and referenceDate is None:
            TermStructure.__init__(self,settlementDays=settlementDays,cal=cal,dc=dc)
            self._bdc = bdc
        else:
            raise RuntimeError('Wrong Parameter!')

    def businessDayConvention(self):
        return self._bdc

    def optionDateFromTenor(self,p):
        return self.calendar().advance(self.referenceDate(),p,self.businessDayConvention())

    def minStrike(self):
        pass

    def maxStrike(self):
        pass

    def checkStrike(self,k,extrapolate):
        if (not extrapolate) and (not self.allowsExtrapolation() and (k<self.minStrike() or k>self.maxStrike())):
            raise RuntimeError('strike  is outside the curve domain ')

