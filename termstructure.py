from mathematics.interpolations.extrapolation import *
from settings import *

'''
检查完毕，无需修改
'''


class TermStructure(Observable, Observer, Extropolator):
    def __init__(self, dc=None, referenceDate=None, cal=None, settlementDays=None):
        Observable.__init__(self)
        Observer.__init__(self)
        Extropolator.__init__(self)
        self._dayCounter = dc
        self._settlementDays = None
        if referenceDate is None and settlementDays is None:
            self._moving = False
            self._updated = True
        elif referenceDate is not None and settlementDays is None:
            self._moving = False
            self._updated = True
            self._calendar = cal
            self._referenceDate = referenceDate
        elif settlementDays is not None and referenceDate is None:
            self._moving = True
            self._updated = False
            self._calendar = cal
            self._settlementDays = settlementDays
            self.registerWith(Settings().evaluationDate())
        else:
            raise RuntimeError('Wrong Parameter!')

    def dayCounter(self):
        return self._dayCounter

    def timeFromReference(self, d):
        return self.dayCounter().yearFraction(self.referenceDate(), d)

    def maxDate(self):
        return datetime.date(2099, 12, 31)

    def maxTime(self):
        return self.timeFromReference(self.maxDate())

    def referenceDate(self):
        if not self._updated:
            today = Settings().evaluationDate()
            self._referenceDate = self.calendar().advance(today, self.settlementDays(), 'Days')
            self._updated = True
        return self._referenceDate

    def calendar(self):
        return self._calendar

    def settlementDays(self):
        if self._settlementDays is None:
            raise RuntimeError('settlement days not provided for this instance')
        return self._settlementDays

    def update(self):
        if self._moving:
            self._updated = False
        self.notifyObservers()

    def checkRange(self, time, extrapolate):
        if isinstance(time, datetime.date):
            if time < self.referenceDate():
                raise RuntimeError('date is before referenceDate')
            if not extrapolate and not self.allowsExtrapolation() and time > self.maxDate():
                raise RuntimeError('date is past max curve date ')
        else:
            if time < 0:
                raise RuntimeError('negative time is given')
            if not extrapolate and not self.allowsExtrapolation() and time > self.maxTime():
                raise RuntimeError('time is past max curve time ')
