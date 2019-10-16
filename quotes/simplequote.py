from quote import *

class SimpleQuote(Quote):
    def __init__(self,value):
        super().__init__()
        self.__value = value

    def value(self):
        if not self.isValid():
            raise RuntimeError('invalid SimpleQuote')
        return self.__value

    def isValid(self):
        return self.__value is not None

    def setValue(self,value):
        if value is None:
            raise RuntimeError('None value!')
        else:
            if self.__value != value:
                self.__value = value
                self.notifyObservers()

    def reset(self):
        self.setValue(None)