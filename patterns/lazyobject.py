from patterns.observable import *

'''
检查完毕，无需修改
'''


class LazyObject(Observable, Observer):
    def __init__(self):
        Observable.__init__(self)
        Observer.__init__(self)
        self._calculated = False
        self._frozen = False
        self._alwaysForward = False

    def update(self):
        if self._calculated or self._alwaysForward:
            self._calculated = False
            if not self._frozen:
                self.notifyObservers()

    def recalculate(self):
        wasFrozen = self._frozen
        self._frozen = False
        self._calculated = False
        try:
            self.calculate()
        except:
            self._frozen = wasFrozen
            self.notifyObservers()
            raise RuntimeError()
        self._frozen = wasFrozen
        self.notifyObservers()

    def freeze(self):
        self._frozen = True

    def unfreeze(self):
        if self._frozen:
            self._frozen = False
            self.notifyObservers()

    def alwaysForwardNotifications(self):
        self._alwaysForward = True

    def calculate(self):
        if (not self._calculated) and (not self._frozen):
            self._calculated = True
            try:
                self.performCalculations()
            except:
                self._calculated = False
                raise RuntimeError()

    def performCalculations(self):
        pass

    def __getitem__(self, position):
        return self._observables[position]
