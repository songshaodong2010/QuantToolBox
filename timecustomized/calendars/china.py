from timecustomized.calendarcustomized import *
from enum import Enum


class China(CalendarCustomized):
    class SseImpl(CalendarCustomized.Impl):
        def name(self):
            return ('Shanghai stock exchange')

        def isWeekend(self, w):
            return w.weekday() == 5 or w.weekday() == 6

        def isBusinessDay(self, dates):
            w = dates.weekday()
            d = dates.day
            m = dates.month
            y = dates.year
            if (w == 5 or w == 6
                    # New Year's Day
                    or (d == 1 and m == 1)
                    or (y == 2005 and d == 3 and m == 1)
                    or (y == 2006 and (d == 2 or d == 3) and m == 1)
                    or (y == 2007 and d <= 3 and m == 1)
                    or (y == 2007 and d == 31 and m == 12)
                    or (y == 2009 and d == 2 and m == 1)
                    or (y == 2011 and d == 3 and m == 1)
                    or (y == 2012 and (d == 2 or d == 3) and m == 1)
                    or (y == 2013 and d <= 3 and m == 1)
                    or (y == 2014 and d == 1 and m == 1)
                    or (y == 2015 and d <= 3 and m == 1)
                    or (y == 2017 and d == 2 and m == 1)
                    or (y == 2018 and d == 1 and m == 1)
                    or (y == 2018 and d == 31 and m == 12)
                    or (y == 2019 and d == 1 and m == 1)
                    # Chinese New Year
                    or (y == 2004 and d >= 19 and d <= 28 and m == 1)
                    or (y == 2005 and d >= 7 and d <= 15 and m == 2)
                    or (y == 2006 and ((d >= 26 and m == 1)
                                       or (d <= 3 and m == 2)))
                    or (y == 2007 and d >= 17 and d <= 25 and m == 2)
                    or (y == 2008 and d >= 6 and d <= 12 and m == 2)
                    or (y == 2009 and d >= 26 and d <= 30 and m == 1)
                    or (y == 2010 and d >= 15 and d <= 19 and m == 2)
                    or (y == 2011 and d >= 2 and d <= 8 and m == 2)
                    or (y == 2012 and d >= 23 and d <= 28 and m == 1)
                    or (y == 2013 and d >= 11 and d <= 15 and m == 2)
                    or (y == 2014 and d >= 31 and m == 1)
                    or (y == 2014 and d <= 6 and m == 2)
                    or (y == 2015 and d >= 18 and d <= 24 and m == 2)
                    or (y == 2016 and d >= 8 and d <= 12 and m == 2)
                    or (y == 2017 and ((d >= 27 and m == 1)
                                       or (d <= 2 and m == 2)))
                    or (y == 2018 and (d >= 15 and d <= 21 and m == 2))
                    or (y == 2019 and d >= 4 and d <= 8 and m == 2)
                    # Ching Ming Festival
                    or (y <= 2008 and d == 4 and m == 4)
                    or (y == 2009 and d == 6 and m == 4)
                    or (y == 2010 and d == 5 and m == 4)
                    or (y == 2011 and d >= 3 and d <= 5 and m == 4)
                    or (y == 2012 and d >= 2 and d <= 4 and m == 4)
                    or (y == 2013 and d >= 4 and d <= 5 and m == 4)
                    or (y == 2014 and d == 7 and m == 4)
                    or (y == 2015 and d >= 5 and d <= 6 and m == 4)
                    or (y == 2016 and d == 4 and m == 4)
                    or (y == 2017 and d >= 3 and d <= 4 and m == 4)
                    or (y == 2018 and d >= 5 and d <= 6 and m == 4)
                    or (y == 2019 and d == 5 and m == 4)
                    # Labor Day
                    or (y <= 2007 and d >= 1 and d <= 7 and m == 5)
                    or (y == 2008 and d >= 1 and d <= 2 and m == 5)
                    or (y == 2009 and d == 1 and m == 5)
                    or (y == 2010 and d == 3 and m == 5)
                    or (y == 2011 and d == 2 and m == 5)
                    or (y == 2012 and ((d == 30 and m == 4) or
                                       (d == 1 and m == 5)))
                    or (y == 2013 and ((d >= 29 and m == 4) or
                                       (d == 1 and m == 5)))
                    or (y == 2014 and d >= 1 and d <= 3 and m == 5)
                    or (y == 2015 and d == 1 and m == 5)
                    or (y == 2016 and d >= 1 and d <= 2 and m == 5)
                    or (y == 2017 and d == 1 and m == 5)
                    or (y == 2018 and ((d == 30 and m == 4) or (d == 1 and m == 5)))
                    or (y == 2019 and d >= 1 and d <= 3 and m == 5)
                    # Tuen Ng Festival
                    or (y <= 2008 and d == 9 and m == 6)
                    or (y == 2009 and (d == 28 or d == 29) and m == 5)
                    or (y == 2010 and d >= 14 and d <= 16 and m == 6)
                    or (y == 2011 and d >= 4 and d <= 6 and m == 6)
                    or (y == 2012 and d >= 22 and d <= 24 and m == 6)
                    or (y == 2013 and d >= 10 and d <= 12 and m == 6)
                    or (y == 2014 and d == 2 and m == 6)
                    or (y == 2015 and d == 22 and m == 6)
                    or (y == 2016 and d >= 9 and d <= 10 and m == 6)
                    or (y == 2017 and d >= 29 and d <= 30 and m == 5)
                    or (y == 2018 and d == 18 and m == 6)
                    or (y == 2019 and d == 7 and m == 6)
                    # Mid-Autumn Festival
                    or (y <= 2008 and d == 15 and m == 9)
                    or (y == 2010 and d >= 22 and d <= 24 and m == 9)
                    or (y == 2011 and d >= 10 and d <= 12 and m == 9)
                    or (y == 2012 and d == 30 and m == 9)
                    or (y == 2013 and d >= 19 and d <= 20 and m == 9)
                    or (y == 2014 and d == 8 and m == 9)
                    or (y == 2015 and d == 27 and m == 9)
                    or (y == 2016 and d >= 15 and d <= 16 and m == 9)
                    or (y == 2018 and d == 24 and m == 9)
                    or (y == 2019 and d == 13 and m == 9)
                    # National Day
                    or (y <= 2007 and d >= 1 and d <= 7 and m == 10)
                    or (y == 2008 and ((d >= 29 and m == 9) or
                                       (d <= 3 and m == 10)))
                    or (y == 2009 and d >= 1 and d <= 8 and m == 10)
                    or (y == 2010 and d >= 1 and d <= 7 and m == 10)
                    or (y == 2011 and d >= 1 and d <= 7 and m == 10)
                    or (y == 2012 and d >= 1 and d <= 7 and m == 10)
                    or (y == 2013 and d >= 1 and d <= 7 and m == 10)
                    or (y == 2014 and d >= 1 and d <= 7 and m == 10)
                    or (y == 2015 and d >= 1 and d <= 7 and m == 10)
                    or (y == 2016 and d >= 3 and d <= 7 and m == 10)
                    or (y == 2017 and d >= 2 and d <= 6 and m == 10)
                    or (y == 2018 and d >= 1 and d <= 5 and m == 10)
                    or (y == 2019 and ((d == 7 and m == 10) or (d >= 1 and d <= 4 and m == 10)))
                    # 70th anniversary of the victory of anti-Japaneses war
                    or (y == 2015 and d >= 3 and d <= 4 and m == 9)):
                return False
            return True

    class IbImpl(CalendarCustomized.Impl):
        def name(self):
            return ('China inter bank market')

        def isWeekend(self, w):
            return w.weekday() == 5 or w.weekday() == 6

        def isBusinessDay(self, d):
            working_weekends = [datetime.date(2019, 2, 2), datetime.date(2019, 2, 3), datetime.date(2019, 4, 28),
                                datetime.date(2019, 5, 5), datetime.date(2019, 9, 29), datetime.date(2019, 10, 12),
                                datetime.date(2018, 2, 11), datetime.date(2018, 2, 24), datetime.date(2018, 4, 8),
                                datetime.date(2018, 4, 28), datetime.date(2018, 9, 20), datetime.date(2018, 9, 30),
                                datetime.date(2018, 12, 29), datetime.date(2017, 1, 22), datetime.date(2017, 2, 4),
                                datetime.date(2017, 4, 1), datetime.date(2017, 5, 27), datetime.date(2017, 9, 30)]
            sseimpl = China.SseImpl()
            return (sseimpl.isBusinessDay(d) or d in working_weekends)

    class Market(Enum):
        SSE = 1
        IB = 2

    def __init__(self, m='SSE'):
        super().__init__()
        if m == self.Market.SSE.name:
            CalendarCustomized.__init__(self,self.SseImpl())
        elif m == self.Market.IB.name:
            CalendarCustomized.__init__(self,self.IbImpl())
        else:
            raise RuntimeError('unknown market')
