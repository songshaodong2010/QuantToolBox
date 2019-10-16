from patterns.observable import *

'''
有点没有弄明白
'''


class StochasticProcess(Observer, Observable):
    class discretization:
        def drift(self, process, t0, x0, dt):
            pass

        def diffusion(self, process, t0, x0, dt):
            pass

        def covariance(self, process, t0, x0, dt):
            pass

    def __init__(self, disc=None):
        Observer.__init__(self)
        Observable.__init__(self)
        self._discretization = disc

    def size(self):
        pass

    def factors(self):
        return self.size()

    def initialValues(self):
        pass

    # 漂移项
    def drift(self, t, x):
        pass

    # 扩散项
    def diffusion(self, t, x):
        pass

    # 返回离散化后随机过程经过dt时间后的期望
    def expectation(self, t0, x0, dt):
        return self.apply(x0, self._discretization.drift(self, t0, x0, dt))

    # 返回离散化后随机过程经过dt时间后的标准差
    def stdDeviation(self, t0, x0, dt):
        return self._discretization.diffusion(self, t0, x0, dt)

    # 返回离散化后随机过程经过dt时间后的协方差
    def covariance(self, t0, x0, dt):
        return self._discretization.covariance(self, t0, x0, dt)

    # 返回离散化后经过dt时间后的资产价值
    def evolve(self, t0, x0, dt, dw):
        return self.apply(self.expectation(t0, x0, dt), self.stdDeviation(t0, x0, dt) * dw)

    # 返回离散化后经过dt时间后的资产价值的变动
    def apply(self, x0, dx):
        return x0 + dx

    # 返回随机过程参照系下的时间价值
    def time(self, d):
        raise RuntimeError('date/time conversion not supported')

    def update(self):
        self.notifyObservers()


class StochasticProcess1D(StochasticProcess):
    class discretization:
        def drift(self, process, t0, x0, dt):
            pass

        def diffusion(self, process, t0, x0, dt):
            pass

        def variance(self, process, t0, x0, dt):
            pass

    def __init__(self, disc=None):
        StochasticProcess.__init__(self, disc=disc)

    def size(self):
        return 1

    def initialValues(self):
        return self.x0()

    def drift(self, t, x):
        return self.drift(t, x)

    def diffusion(self, t, x):
        return self.diffusion(t, x)

    def expectation(self, t0, x0, dt):
        return self.apply(x0, self._discretization.drift(self, t0, x0, dt))

    def stdDeviation(self, t0, x0, dt):
        return self._discretization.diffusion(self, t0, x0, dt)

    def covariance(self, t0, x0, dt):
        return self.covariance(t0, x0, dt)

    def variance(self, t0, x0, dt):
        return self._discretization.variance(self, t0, x0, dt)

    def evolve(self, t0, x0, dt, dw):
        return self.evolve(t0, x0, dt, dw)

    def apply(self, x0, dx):
        return x0 + dx

    def x0(self):
        pass
