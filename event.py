from patterns.observable import *
from settings import *


class Event(Observable):
    def hasOccurred(self, d=None, includeRefDate=False):
        refDate = d if d is not None else Settings().evaluationDate()
        includeRefDateEvent = includeRefDate if includeRefDate else Settings().includeReferenceDateEvents()
        if includeRefDateEvent:
            return self.date() < refDate
        else:
            return self.date() <= refDate

    def date(self):
        pass


class SimpleEvent(Event):
    def __init__(self, date):
        Event.__init__(self)
        self._date = date

    def date(self):
        return self._date
