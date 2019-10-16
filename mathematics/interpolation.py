from mathematics.interpolations.extrapolation import *


class Interpolation(Extropolator):
    class Impl:
        def update(self):
            pass

        def xMin(self):
            pass

        def xMax(self):
            pass

        def xValues(self):
            pass

        def yValues(self):
            pass

        def isInRange(self,x):
            pass

        def value(self):
            pass

        def primitive(self):
            pass

        def derivative(self):
            pass

        def secondDerivative(self):
            pass

    class templateImpl(Impl):
        def __init__(self, xBegin, xEnd, yBegin, requiredPoints=2):
            self._xBegin = xBegin
            self._xEnd = xEnd
            self._yBegin = yBegin

        def xMin(self):
            return self._xBegin

        def xMax(self):
            return self._xEnd

        def xValues(self):
            return (self._xBegin,self._xEnd)

        def yValues(self):
            return (self._yBegin,self._yBegin+(self._xEnd-self._xBegin))

        def isInRange(self,x):
            x1=self.xMin()
            x2=self.xMax()
            return (x >= x1 and x<=x2) or self.close(x,x1) or self.close(x,x2)

