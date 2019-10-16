from timecustomized.frequency import *
import numpy as np

'''
检查完毕，无需修改
'''


class InterestRate:
    def __init__(self, r=None, dc=None, comp=None, freq=None):
        if r is None and dc is None and comp is None and freq is None:
            pass
        elif r is not None and dc is not None and comp is not None and freq is not None:
            self._r = r
            self._dc = dc
            self._comp = comp
            self._freqMakesSense = False
            if self._comp.name == 'Compounded' or self._comp.name == 'SimpleThenCompounded' or self._comp.name == 'CompoundedThenSimple':
                self._freqMakesSense = True
                if self._freq.name == 'Once' and self._freq.name == 'NoFrequency':
                    raise RuntimeError('frequency not allowed for this interest rate')
                self._freq = freq.value
        else:
            raise RuntimeError('Wrong Parameter!')

    def Rate(self):
        return self._r

    def dayCounter(self):
        return self._dc

    def compounding(self):
        return self._comp

    def frequency(self):
        if self._freqMakesSense:
            return Frequency(self._freq)
        else:
            return Frequency.NoFrequency

    def discountFactor(self, t=None, d1=None, d2=None, refStart=None, refEnd=None):
        if t is not None and d1 is None and d2 is None:
            return 1.0 / self.compoundFactor(t=t)
        elif t is None and d1 is not None and d2 is not None:
            if d1 > d2:
                raise RuntimeError('d1 later than d2 ')
            t = self._dc.yearFraction(d1, d2, refStart=refStart, refEnd=refEnd)
            return self.discountFactor(t=t)
        else:
            raise RuntimeError('wrong parameter')

    def compoundFactor(self, t=None, d1=None, d2=None, refStart=None, refEnd=None):
        if t is not None and d1 is None and d2 is None:
            if t < 0:
                raise RuntimeError('negative time not allowed')
            if self._r is None:
                raise RuntimeError('null interest rate')
            if self._comp.name == 'Simple':
                return 1 + self._r * t
            elif self._comp.name == 'Compounded':
                return pow(1 + self._r / self._freq, self._freq * t)
            elif self._comp.name == 'Continuous':
                return np.exp(self._r * t)
            elif self._comp.name == 'SimpleThenCompounded':
                if t <= 1.0 / self._freq:
                    return 1.0 + self._r * t
                else:
                    return pow(1 + self._r / self._freq, self._freq * t)
            elif self._comp.name == 'CompoundedThenSimple':
                if t > 1.0 / self._freq:
                    return 1.0 + self._r * t
                else:
                    return pow(1 + self._r / self._freq, self._freq * t)
            else:
                raise RuntimeError('unknown compounding convention')
        elif t is None and d1 is not None and d2 is not None:
            if d1 > d2:
                raise RuntimeError('d1 later than d2 ')
            t = self._dc.yearFraction(d1, d2, refStart=refStart, refEnd=refEnd)
            return self.compoundFactor(t=t)
        else:
            raise RuntimeError('wrong parameter')

    def impliedRate(self, compound, resultDC, comp, freq, t=None, d1=None, d2=None, refStart=None, refEnd=None):
        if t is not None and d1 is None and d2 is None:
            if compound <= 0:
                raise RuntimeError('positive compound factor required')
            r = None
            if compound == 1.0:
                if t < 0:
                    raise RuntimeError('non negative time required')
                r = 0.0
            else:
                if t <= 0:
                    raise RuntimeError('positive time required')
                if comp.name == 'Simple':
                    r = (compound - 1.0) / t
                elif comp.name == 'Compounded':
                    r = (pow(compound, 1.0 / (freq.value * t)) - 1) * freq.value
                elif comp.name == 'Continuous':
                    r = np.log(compound) / t
                elif comp.name == 'SimpleThenCompounded':
                    if t <= 1.0 / freq.value:
                        r = (compound - 1.0) / t
                    else:
                        r = (pow(compound, 1.0 / (freq.value * t)) - 1) * freq.value
                elif comp.name == 'CompoundedThenSimple':
                    if t > 1.0 / freq.value:
                        r = (compound - 1.0) / t
                    else:
                        r = (pow(compound, 1.0 / (freq.value * t)) - 1) * freq.value
                else:
                    raise RuntimeError('unknown compounding convention')
            return InterestRate(r, resultDC, comp, freq)
        elif t is None and d1 is not None and d2 is not None:
            if d1 > d2:
                raise RuntimeError('d1 later than d2 ')
            t = resultDC.yearFraction(d1, d2, refStart=refStart, refEnd=refEnd)
            return self.impliedRate(compound, resultDC, comp, freq, t=t)

    def equivalentRate(self, comp, freq, resultDC=None, t=None, d1=None, d2=None, refStart=None, refEnd=None):
        if t is not None and resultDC is None and d1 is None and d2 is None:
            return self.impliedRate(self.compoundFactor(t=t), self._dc, comp, freq, t=t)
        elif t is None and resultDC is not None and d1 is not None and d2 is not None:
            if d1 > d2:
                raise RuntimeError('d1 later than d2 ')
            t1 = self._dc.yearFraction(d1, d2, refStart=refStart, refEnd=refEnd)
            t2 = resultDC.yearFraction(d1, d2, refStart=refStart, refEnd=refEnd)
            return self.impliedRate(self.compoundFactor(t=t1), resultDC, comp, freq, t=t2)
