from timecustomized.daycounter import *
from timecustomized.calendarcustomized import *
from timecustomized.calendars.china import *


def sameYear(d1, d2):
    return d1.year == d2.year


def sameMonth(d1, d2):
    return d1.year == d2.year and d1.month == d2.month


def businessDays():
    pass


class Business252(DayCounter):
    class Impl(DayCounter.Impl):
        def __init__(self, c=None):
            super().__init__()
            self.__calendar = c

        def name(self):
            result = 'Business/252(' + self.__calendar.name() + ')'
            return result

        def dayCount(self, d1, d2):
            if (sameMonth(d1, d2) or d1 >= d2):
                return self.__calendar.businessDaysBetween(d1, d2)
            elif sameYear(d1, d2):
                total = 0
                if d1.month in range(1, 12):
                    d = datetime.date(d1.year, d1.month + 1, 1)
                else:
                    d = datetime.date(d1.year + 1, 1, 1)
                total = total + self.__calendar.businessDaysBetween(d1, d)
                while not sameMonth(d, d2):
                    da1 = datetime.date(d.year, d.month, 1)
                    if d.month in range(1, 12):
                        da2 = datetime.date(d1.year, d1.month + 1, 1)
                    else:
                        da2 = datetime.date(d1.year + 1, 1, 1)
                    temp = self.__calendar.businessDaysBetween(da1, da2)
                    total = total + temp
                    if d.month in range(1, 12):
                        d = datetime.date(d.year, d.month + 1, 1)
                    else:
                        d = datetime.date(d.year + 1, 1, 1)
                total = total + self.__calendar.businessDaysBetween(d, d2)
                return total
            else:
                total = 0
                if d1.month in range(1, 12):
                    d = datetime.date(d1.year, d1.month + 1, 1)
                else:
                    d = datetime.date(d1.year + 1, 1, 1)
                total = total + self.__calendar.businessDaysBetween(d1, d)
                for m in range(d1.month + 1, 12):
                    da1 = datetime.date(d.year, m, 1)
                    if d.month in range(1, 12):
                        da2 = datetime.date(d1.year, m + 1, 1)
                    else:
                        da2 = datetime.date(d1.year + 1, 1, 1)
                    temp = self.__calendar.businessDaysBetween(da1, da2)
                    total = total + temp
                d = datetime.date(d1.year + 1, 1, 1)
                while not sameYear(d, d2):
                    for m in range(1, 13):
                        total = total + calendar.monthrange(d.year, d.month)
                    d = datetime.date(d.year + 1, 1, 1)
                for m in range(1, d2.month):
                    total = total + calendar.monthrange(d.year, d.month)
                d = datetime.date(d2.year, d2.month, 1)
                total = total + self.__calendar.businessDaysBetween(d, d2)
            return total

        def yearFraction(self, d1, d2, refPeriodStart=None, refPeriodEnd=None):
            return self.dayCount(d1, d2) / 252.0

    def __init__(self, c=China()):
        super().__init__(self.Impl(c))
