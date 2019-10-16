from enum import Enum
from datetime import datetime

'''
检查完毕，无需修改
'''

class Exercise:
    class Type(Enum):
        American = 1
        Bermudan = 2
        European = 3

    def __init__(self, type):
        self._type = type
        self._dates = None

    def Exercise(self):
        pass

    def type(self):
        return self._type

    def date(self, index):
        return self._dates[index]

    def dates(self):
        return self._dates

    def lastDate(self):
        return self._dates[-1]


class EarlyExercise(Exercise):
    def __init__(self, type, payoffAtExpiry=False):
        Exercise.__init__(self, type)
        self._payoffAtExpiry = payoffAtExpiry

    def payoffAtExpiry(self):
        return self._payoffAtExpiry


class AmericanExercise(EarlyExercise):
    def __init__(self, latest, earliest=None, payoffAtExpiry=False):
        EarlyExercise.__init__(self, Exercise.Type.American, payoffAtExpiry=payoffAtExpiry)
        if earliest is not None:
            self._dates = list()
            self._dates.append(earliest)
            self._dates.append(latest)
        else:
            self._dates = list()
            self._dates.append(datetime(1900, 1, 1))
            self._dates.append(latest)


class BermudanExercise(EarlyExercise):
    def __init__(self, dates, payoffAtExpiry=False):
        EarlyExercise.__init__(self, Exercise.Type.Bermudan, payoffAtExpiry=payoffAtExpiry)
        if dates:
            dates.sort()
            self._dates = list()
            for item in dates:
                self._dates.append(item)


class EuropeanExercise(Exercise):
    def __init__(self, date):
        Exercise.__init__(self, Exercise.Type.European)
        self._dates = list()
        self._dates.append(date)
