import datetime
import calendar
import collections
from timecustomized.businessdayconvention import BusinessDayConvention


class CalendarCustomized:
    class Impl:
        def __init__(self):
            self.addedHolidays = collections.deque()
            self.removedHolidays = collections.deque()

        def name(self):
            pass

        def isBusinessDay(self, d):
            pass

        def isWeekend(self, w):
            pass

    def __init__(self, impl=None):
        self._impl = impl

    # 判断日历函数是否初始化
    def empty(self):
        return (self._impl is None)

    # 返回日历函数的类型
    def name(self):
        if self._impl is None:
            raise RuntimeError('no implementation provided')
        else:
            return self._impl.name()

    # 返回日历中添加的节假日
    def addedHolidays(self):
        if self._impl is None:
            raise RuntimeError('no implementation provided')
        else:
            return self._impl.addedHolidays

    # 返回日历中移除的节假日
    def removedHolidays(self):
        if self._impl is None:
            raise RuntimeError('no implementation provided')
        else:
            return self._impl.removedHolidays

    # 返回输入日期是否是工作日
    def isBusinessDay(self, d):
        if self._impl is None:
            raise RuntimeError('no implementation provided')
        else:
            if d in self._impl.addedHolidays:
                return False
            if d in self._impl.removedHolidays:
                return True
            return self._impl.isBusinessDay(d)

    # 返回输入日期是否是节假日
    def isHoliday(self, d):
        return (not self.isBusinessDay(d))

    # 返回输入日期是否是周末
    def isWeekend(self, w):
        if self._impl is None:
            raise RuntimeError('no implementation provided')
        else:
            return self._impl.isWeekend(w)

    # 返回输入日期是否是当月最后一个工作日
    def isEndOfMonth(self, d):
        return (d.month != self.adjust(d + datetime.timedelta(1)).month)

    # 返回输入日期的月份的最后一个工作日
    def endOfMonth(self, d):
        return self.adjust(datetime.date(d.year, d.month, calendar.monthrange(d.year, d.month)[1]),
                           BusinessDayConvention.Preceding)

    # 增加一个节假日的日期
    def addHoliday(self, d):
        if self._impl is None:
            raise RuntimeError('no implementation provided')
        else:
            self._impl.removedHolidays(d)
            if self._impl.isBusinessDay(d):
                self._impl.addedHolidays.append(d)

    # 移除一个节假日的日期
    def removeHoliday(self, d):
        if self._impl is None:
            raise RuntimeError('no implementation provided')
        else:
            self._impl.addedHolidays.remove(d)
            if (not self._impl.isBusinessDay(d)):
                self._impl.removedHolidays.append(d)

    # 获取一个非工作日的最近工作日的日期
    def adjust(self, d, c=BusinessDayConvention.Following):
        if d == None:
            raise RuntimeError("Null Date")
        else:
            if c.name == 'Unadjusted':
                return d
            d1 = d
            if c.name == 'Following' or c.name == 'ModifiedFollowing':
                while self.isHoliday(d1):
                    d1 = d1 + datetime.timedelta(1)
                if c.name == 'ModifiedFollowing':
                    if d1.month != d.month:
                        return self.adjust(d, BusinessDayConvention.Preceding)
            elif c.name == 'Preceding' or c.name == 'ModifiedPreceding':
                while self.isHoliday(d1):
                    d1 = d1 - datetime.timedelta(1)
                if (c.name == 'ModifiedPreceding' and (d1.month != d.month)):
                    return self.adjust(d, BusinessDayConvention.Following)
            elif c.name == 'Nearest':
                d2 = d
                while (self.isHoliday(d1) and self.isHoliday(d2)):
                    d1 = d1 + datetime.timedelta(1)
                    d2 = d2 - datetime.timedelta(1)
                if self.isHoliday(d1):
                    return d2
                else:
                    return d1
            else:
                raise RuntimeError('unknown business-day convention')
            return d1

    # 获取推迟给定周期下的工作日
    def advance(self, d, n, unit, c=BusinessDayConvention.Following, endOfMonth=False):
        if d is None:
            raise RuntimeError('Null Date')
        else:
            if n == 0:
                return self.adjust(d, c)
            elif unit == 'days':
                d1 = d
                if n > 0:
                    while n > 0:
                        d1 = d1 + datetime.timedelta(1)
                        while self.isHoliday(d1):
                            d1 = d1 + datetime.timedelta(1)
                        n = n - 1
                else:
                    while n < 0:
                        d1 = d1 - datetime.timedelta(1)
                        while self.isHoliday(d1):
                            d1 = d1 - datetime.timedelta(1)
                        n = n + 1
                return d1
            elif unit == 'weeks':
                d1 = d + datetime.timedelta(n * 7)
                return self.adjust(d1, c)
            else:
                raise RuntimeError('not apply Month and Year')

    # 获取两个日期之间的工作日的天数
    def businessDaysBetween(self, begin, end, includeFirst=True, includeLast=False):
        wd = 0
        if begin != end:
            if begin < end:
                begin1 = begin + datetime.timedelta(1)
                end1 = end
                while begin1 < end1:
                    if (self.isBusinessDay(begin1)):
                        wd += 1
                    begin1 = begin1 + datetime.timedelta(1)
                if self.isBusinessDay(end):
                    wd += 1
            elif begin > end:
                begin2 = begin
                end2 = end + datetime.timedelta(1)
                while end2 < begin2:
                    if (self.isBusinessDay(end2)):
                        wd += 1
                    end2 = end2 + datetime.timedelta(1)
                if self.isBusinessDay(begin2):
                    wd += 1
            if (self.isBusinessDay(begin) and (not includeFirst)):
                wd -= 1
            if (self.isBusinessDay(end) and (not includeLast)):
                wd -= 1
            if begin > end:
                wd = -wd
        elif (includeFirst and includeLast and self.isBusinessDay(begin)):
            wd = 1
        return wd
