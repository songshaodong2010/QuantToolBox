from patterns.observable import *


class ObservableValue:
    def __init__(self,t=None):
        if t is None:
            self._value = None
            self._observable = Observable()
        elif isinstance(t,ObservableValue):
            self._value = t.value()
            self._observable = Observable()
        else:
            self._value = t
            self._observable = Observable()

    def setValue(self,t):
        if isinstance(t,ObservableValue):
            self._value = t.value()
            self._observable.notifyObservers()
        else:
            self._value = t
            self._observable.notifyObservers()

    def value(self):
        return self._value

    def __call__(self, *args, **kwargs):
        return self._observable


