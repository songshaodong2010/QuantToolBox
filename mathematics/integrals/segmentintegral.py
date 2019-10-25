from mathematics.integrals.integrals import *


class SegmentIntegral(Integrator):
    def __init__(self, intervals):
        Integrator.__init__(self, 1, 1)
        self._intervals = intervals
        if intervals <= 0:
            raise RuntimeError('at least 1 interval needed, 0 given')

    def integrate(self, f, a, b):
        if abs(a - b) < 10 ^ -9:
            return 0
        dx = (b - a) / self._intervals
        sum = 0.5 * (f(a) + f(b))
        end = b - 0.5 * dx
        for x in range(a + dx, end, dx):
            sum += f(x)
        return sum * dx
