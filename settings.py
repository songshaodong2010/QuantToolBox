from patterns.singleton import Singleton
from utilities.observablevalue import *
import datetime

'''
用来程序运行时存储全局设定的类
'''
class Settings(Singleton):
    def __init__(self):
        Singleton.__init__(self,self)
        self._includeReferenceDateEvents = False
        self._enforcesTodaysHistoricFixings = False
        self._evaluationDate = ObservableValue()
        self._includeTodaysCashFlows = None

    def setEvaluationDate(self,d):
        self._evaluationDate.setValue(d)

    def evaluationDate(self):
        if self._evaluationDate.value() is None:
            self._evaluationDate.setValue(datetime.datetime.date(datetime.datetime.now()))
        return self._evaluationDate.value()

    def anchorEvaluationDate(self):
        if self._evaluationDate.value() is None:
            self._evaluationDate.setValue(datetime.datetime.date(datetime.datetime.now()))

    def resetEvaluationDate(self):
        self._evaluationDate = None

    def includeReferenceDateEvents(self):
        return self._includeReferenceDateEvents

    def includeTodaysCashFlows(self):
        return self._includeTodaysCashFlows

    def enforcesTodaysHistoricFixings(self):
        return self._enforcesTodaysHistoricFixings

class SavedSettings:
    def __init__(self):
        self._evaluationDate =  Settings().evaluationDate()
        self._includeReferenceDateEvents = Settings().includeReferenceDateEvents()
        self._includeTodaysCashFlows = Settings().includeTodaysCashFlows()
        self._enforcesTodaysHistoricFixings = Settings().enforcesTodaysHistoricFixings()
