from termstructure import *
from interestrate import *

'''
检查完毕，无需修改
'''
dt = 0.0001


class YieldTermStructure(TermStructure):
    def __init__(self, dc=None, referenceDate=None, settlementDays=None, cal=None):
        if referenceDate is None and settlementDays is None:
            TermStructure.__init__(self, dc=dc)
        elif referenceDate is not None and settlementDays is None:
            TermStructure.__init__(self, dc=dc, referenceDate=referenceDate, cal=cal)
        elif referenceDate is None and settlementDays is not None:
            TermStructure.__init__(self, dc=dc, settlementDays=settlementDays, cal=cal)
        else:
            raise RuntimeError('Wrong Parameter!')
        self._jumps = list()
        self._jumpDates = list()
        self._jumpTimes = [0 for i in range(len(self._jumpDates))]
        self._nJumps = [0 for i in range(len(self._jumps))]
        self._latestReference = None
        self.setJumps()
        for i in range(len(self._nJumps)):
            self.registerWith(self._jumps[i])

    def setJumps(self):
        if not self._jumpDates and (self._jumps):
            self._jumpDates = [0 for i in range(len(self._nJumps))]
            self._jumpTimes = [0 for i in range(len(self._nJumps))]
            y = self.referenceDate().year
            for i in range(len(self._nJumps)):
                self._jumpDates[i] = datetime.date(y + i, 12, 31)
        else:
            if len(self._jumpDates) != len(self._nJumps):
                raise RuntimeError('mismatch between number of jumps  and jump dates')
        for i in range(len(self._nJumps)):
            self._jumpTimes[i] = self.timeFromReference(self._jumpDates[i])
        self._latestReference = self.referenceDate()

    def discount(self, time, extrapolate=False):
        if isinstance(time, datetime.date):
            t = self.timeFromReference(time)
        else:
            t = time
        self.checkRange(t, extrapolate)
        if not self._jumps:
            return self.discountImpl(t)
        jumpEffect = 1.0
        for i in range(len(self._nJumps)):
            if (self._jumpTimes[i] > 0 and self._jumpTimes[i] < t):
                thisJump = self._jumps[i].value()
                jumpEffect = jumpEffect * thisJump
        return jumpEffect * self.discountImpl(t)

    def zeroRate(self, comp, freq, extrapolate=False, d=None, dayCounter=None, t=None):
        if d is not None and dayCounter is not None and t is None:
            if d == self.referenceDate():
                compound = 1.0 / self.discount(dt, extrapolate)
                return InterestRate().impliedRate(compound, dayCounter, comp, freq, t=dt)
            compound = 1.0 / self.discount(d, extrapolate)
            return InterestRate().impliedRate(compound, dayCounter, comp, freq, d1=self.referenceDate(), d2=d)
        if d is None and dayCounter is None and t is not None:
            if t == 0:
                t = dt
            compound = 1.0 / self.discount(t, extrapolate)
            return InterestRate().impliedRate(compound, self.dayCounter(), comp, freq, t=t)

    def forwardRate(self, comp, freq, extrapolate=False, d1=None, d2=None, dayCounter=None, t1=None, t2=None):
        if d1 is not None and d2 is not None and dayCounter is not None and t1 is None and t2 is None:
            if d1 == d2:
                self.checkRange(d1, extrapolate)
                t1 = max(self.timeFromReference(d1) - dt / 2, 0)
                t2 = t1 + dt
                compound = self.discount(t1, True) / self.discount(t2, True)
                return InterestRate().impliedRate(compound, dayCounter, comp, freq, t=dt)
            else:
                if d1 > d2:
                    raise RuntimeError('d1  later than  d2')
                compound = self.discount(d1, extrapolate) / self.discount(d2, extrapolate)
                return InterestRate().impliedRate(compound, dayCounter, comp, freq, d1=d1, d2=d2)
        elif d1 is None and d2 is None and dayCounter is None and t1 is not None and t2 is not None:
            if t1 == t2:
                self.checkRange(t1, extrapolate)
                t1 = max(t1 - dt / 2, 0)
                t2 = t1 + dt
                compound = self.discount(t1, True) / self.discount(t2, True)
            else:
                if t1 > t2:
                    raise RuntimeError('t1 > t2')
                compound = self.discount(t1, extrapolate) / self.discount(t2, extrapolate)
            return InterestRate().impliedRate(compound, self.dayCounter(), comp, freq, t=t2 - t1)
        else:
            raise RuntimeError('Wrong Parameter!')

    def update(self):
        TermStructure.update(self)
        newReference = None
        try:
            newReference = self.referenceDate()
            if newReference != self._latestReference:
                self.setJumps()
        except:
            if newReference is None:
                return
            else:
                raise RuntimeError()

    def discountImpl(self, t):
        pass
