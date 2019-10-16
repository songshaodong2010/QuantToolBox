import datetime


class DayCounter:
    class Impl:
        def name(self):
            pass

        def dayCount(self, d1, d2):
            return (d2 - d1).days

        def yearFraction(self, d1, d2, refPeriodStart=None, refPeriodEnd=None):
            pass

    def __init__(self, impl=None):
        self._impl = impl

    # 返回dayCounter是否初始化
    def empty(self):
        return (self._impl is None)

    def name(self):
        if self._impl is None:
            raise RuntimeError('no implementation provided')
        else:
            return self._impl.name()

    def dayCount(self, d1, d2):
        if self._impl is None:
            raise RuntimeError('no implementation provided')
        else:
            return self._impl.dayCount(d1, d2)

    def yearFraction(self, d1, d2, refPeriodStart=None, refPeriodEnd=None):
        if self._impl is None:
            raise RuntimeError('no implementation provided')
        else:
            return self._impl.yearFraction(d1, d2, refPeriodStart=refPeriodStart, refPeriodEnd=refPeriodEnd)
