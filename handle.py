from patterns.observable import *


class Handle:
    class Link(Observer, Observable):
        def __init__(self, h, registerAsObserver):
            Observable.__init__(self)
            Observer.__init__(self)
            self._isObserver = False
            self._h = list()
            self.linkTo(h, registerAsObserver)

        def linkTo(self, h, registerAsObserver):
            if (h != self._h or self._isObserver != registerAsObserver):
                if (self._h and self._isObserver):
                    self.unregisterWith(self._h)
                self._h = h
                self._isObserver = registerAsObserver
                if (self._h and self._isObserver):
                    self.registerWith(self._h)
                self.notifyObservers()

        def empty(self):
            return self._h is None

        def currentLink(self):
            if self.empty():
                raise RuntimeError('empty Handle cannot be dereferenced')
            return self._h

        def update(self):
            self.notifyObservers()

    def __init__(self, p=None, registerAsObserver=True):
        if p is None:
            p = list()
        self._link = self.Link(p, registerAsObserver)

    def currentLink(self):
        if self.empty():
            raise RuntimeError('empty Handle cannot be dereferenced')
        return self._link.currentLink()

    def empty(self):
        return self._link.empty()

    def __eq__(self, other):
        return self._link == other._link

    def __ne__(self, other):
        return self._link != other._link

    def __lt__(self, other):
        return self._link < other._link

    def __call__(self, *args, **kwargs):
        return self._link.currentLink()


class RelinkableHandle(Handle):
    def __init__(self, p, registerAsObserver=True):
        Handle.__init__(self, p, registerAsObserver)

    def linkTo(self, h, registerAsObserver=True):
        return self._link.linkTo(h, registerAsObserver)
