from patterns.singleton import *

'''
检查完毕，setChange还需要修改
'''


# 运行时的全局访问点
class ObservableSettings(Singleton):
    def __init__(self):
        super().__init__(self)
        self._deferredObservers = list()
        self._updatesEnabled = True
        self._updatesDeferred = False

    def disableUpdates(self, deferred=False):
        self._updatesEnabled = False
        self._updatesDeferred = deferred

    def enableUpdates(self):
        self._updatesEnabled = True
        self._updatesDeferred = False
        if self._deferredObservers:
            successful = True
            errMsg = ''
            for item in self._deferredObservers:
                try:
                    item.update()
                except Exception as e:
                    successful = False
                    errMsg = e.args[0]
            self._deferredObservers.clear()
            if not successful:
                raise RuntimeError('could not notify one or more observers:' + errMsg)

    def updatesEnabled(self):
        return self._updatesEnabled

    def updatesDeferred(self):
        return self._updatesDeferred

    def registerDeferredObservers(self, observers):
        if self._updatesDeferred:
            for item in observers:
                self._deferredObservers.append(item)

    def unregisterDeferredObserver(self, o):
        self._deferredObservers.remove(o)

    def __getitem__(self, position):
        return self._deferredObservers[position]


class Observable:
    def __init__(self):
        self._observers = list()
        self._settings = ObservableSettings()

    def notifyObservers(self):
        if not self._settings.updatesEnabled():
            self._settings.registerDeferredObservers(self._observers)
        elif self._observers:
            successful = True
            errMsg = ''
            for item in self._observers:
                try:
                    item.update()
                except Exception as e:
                    errMsg = e.args[0]
                    successful = False
            if not successful:
                raise RuntimeError('could not notify one or more observers:' + errMsg)

    def registerObserver(self, o):
        self._observers.append(o)

    def unregisterObserver(self, o):
        if self._settings.updatesDeferred():
            self._settings.unregisterDeferredObserver(o)
        self._observers.remove(o)

    # setChange还需要修改
    def setChange(self, o):
        if self is not o:
            self.notifyObservers()

    def __getitem__(self, position):
        return self._observers[position]


class Observer:
    def __init__(self, o=None):
        if o is None:
            self._observables = list()
        else:
            self._observables = o._observables
            for item in self._observables:
                item.registerObserver(self)

    def changeObservable(self, o):
        for item in self._observables:
            item.unregisterObserver(self)
        self._observables = o._observables
        for item in self._observables:
            item.registerObserver(self)

    def registerWith(self, h):
        if h:
            h.registerObserver(self)
            self._observables.append(h)

    def registerWithObservables(self, o):
        if o:
            for item in o.observables:
                self.registerWith(item)

    def unregisterWith(self, h):
        if h:
            h.unregisterObserver(self)
            self._observables.remove(h)

    def unregisterWithAll(self):
        for i in self._observables:
            i.unregisterObserver(self)
        self._observables.clear()

    def update(self):
        pass

    def deepUpdate(self):
        self.update()

    def __getitem__(self, position):
        return self._observables[position]
