from timecustomized.calendarcustomized import *

class NullCalendar(CalendarCustomized):
    class Impl(CalendarCustomized.Impl):
        def name(self):
            return 'Null'

        def isWeekend(self, w):
            return False

        def isBusinessDay(self, d):
            return True

    def __init__(self):
        CalendarCustomized.__init__(self,impl=self.Impl())