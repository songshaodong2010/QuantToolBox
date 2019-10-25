from stochasticprocess import *
from termstructures.yieldtermstructure import *
from processes.eulerdiscretization import *
from enum import Enum
from compounding import *
import math


class HestonProcess(StochasticProcess):
    class Discretization(Enum):
        PartialTruncation = 1
        FullTruncation = 2
        Reflection = 3
        NonCentralChiSquareVariance = 4
        QuadraticExponential = 5
        QuadraticExponentialMartingale = 6
        BroadieKayaExactSchemeLobatto = 7
        BroadieKayaExactSchemeLaguerre = 8
        BroadieKayaExactSchemeTrapezoidal = 9

    def __init__(self, riskFreeRate, dividendYield, s0, v0, kappa, theta, sigma, rho,
                 d=Discretization.QuadraticExponentialMartingale):
        StochasticProcess.__init__(self, disc=EulerDiscretization())
        self._riskFreeRate = riskFreeRate
        self._dividendYield = dividendYield
        self._s0 = s0
        self._v0 = v0
        self._kappa = kappa
        self._theta = theta
        self._sigma = sigma
        self._rho = rho
        self._discretization = d
        self.registerWith(self._riskFreeRate)
        self.registerWith(self._dividendYield)
        self.registerWith(self._s0)

    def size(self):
        return 2

    def factors(self):
        return 3 if (
                self._discretization == self.Discretization.BroadieKayaExactSchemeLobatto
                or self._discretization == self.Discretization.BroadieKayaExactSchemeTrapezoidal
                or self._discretization == self.Discretization.BroadieKayaExactSchemeLaguerre) \
            else 2

    def initialValues(self):
        tmp = [0] * 2
        tmp[0] = self._s0.value()
        tmp[1] = self._v0
        return tmp

    def drift(self, t, x):
        tmp = [0] * 2
        vol = np.sqrt(x[1]) if x[1] > 0 else (
            -np.sqrt(-x[1]) if self._discretization == self.Discretization.Reflection else 0)
        tmp[0] = self._riskFreeRate.forwardRate(t, t, Compounding.Continuous) \
                 - self._dividendYield.forwardRate(t, t, Compounding.Continuous) - 0.5 * vol * vol
        tmp[1] = self._kappa * (self._theta - (
            x[1] if self._discretization == self.Discretization.PartialTruncation else vol * vol))
        return tmp

    def diffusion(self, t, x):
        tmp = [[0, 0], [0.0]]
        vol = np.sqrt(x[1]) if x[1] > 0 else (
            -np.sqrt(-x[1]) if self._discretization == self.Discretization.Reflection else 1e-8)
        sigma2 = self._sigma * vol
        sqrthov = np.sqrt(1 - self._rho * self._rho)
        tmp[0][0] = vol
        tmp[0][1] = 0
        tmp[1][0] = self._rho * sigma2
        tmp[1][1] = sqrthov * sigma2
        return tmp

    def apply(self, x0, dx):
        tmp = [0] * 2
        tmp[0] = x0[0] * np.exp(dx[0])
        tmp[1] = x0[1] * dx[1]
        return tmp

    def evolve(self, t0, x0, dt, dw):
        retVal = [0] * 2
        sdt = np.sqrt(dt)
        sqrthov = np.sqrt(1 - self._rho * self._rho)
        if self._discretization == self.Discretization.PartialTruncation:
            vol = np.sqrt(x0[1]) if x0[1] > 0 else 0
            vol2 = self._sigma * vol
            mu = self._riskFreeRate.forwardRate(t0, t0 + dt, Compounding.Continuous) - self._dividendYield.forwardRate(
                t0, t0 + dt, Compounding.Continuous) - 0.5 * vol * vol
            nu = self._kappa * (self._theta - x0[1])
            retVal[0] = x0[0] * np.exp(mu * dt + vol * dw[0] * sdt)
            retVal[1] = x0[1] + nu * dt + vol2 * sdt * (self._rho * dw[0] + sqrthov * dw[1])
        elif self._discretization == self.Discretization.FullTruncation:
            vol = np.sqrt(x0[1]) if x0[1] > 0 else 0
            vol2 = self._sigma * vol
            mu = self._riskFreeRate.forwardRate(t0, t0 + dt, Compounding.Continuous) - self._dividendYield.forwardRate(
                t0, t0 + dt, Compounding.Continuous) - 0.5 * vol * vol
            nu = self._kappa * (self._theta - vol * vol)
            retVal[0] = x0[0] * np.exp(mu * dt + vol * dw[0] * sdt)
            retVal[1] = x0[1] + nu * dt + vol2 * sdt * (self._rho * dw[0] + sqrthov * dw[1])
        elif self._discretization == self.Discretization.Reflection:
            vol = np.sqrt(abs(x0[1]))
            vol2 = self._sigma * vol
            mu = self._riskFreeRate.forwardRate(t0, t0 + dt, Compounding.Continuous) - self._dividendYield.forwardRate(
                t0, t0 + dt, Compounding.Continuous) - 0.5 * vol * vol
            nu = self._kappa * (self._theta - vol * vol)
            retVal[0] = x0[0] * np.exp(mu * dt + vol * dw[0] * sdt)
            retVal[1] = vol * vol + nu * dt + vol2 * sdt * (self._rho * dw[0] + sqrthov * dw[1])
        elif self._discretization == self.Discretization.NonCentralChiSquareVariance:
            vol = np.sqrt(x0[1]) if x0[1] > 0 else 0
            mu = self._riskFreeRate.forwardRate(t0, t0 + dt, Compounding.Continuous) - self._dividendYield.forwardRate(
                t0, t0 + dt, Compounding.Continuous) - 0.5 * vol * vol
            retVal[1] = varianceDistribution(x0[1], dw[1], dt)
            dy = (mu - self._rho / self._sigma * self._kappa * (self._theta - vol * vol) * dt + vol * sqrthov * dw[
                0] * sdt)
            retVal[0] = x0[0] * np.exp(dy + self._rho / self._sigma * (retVal[1] - x0[1]))
        elif self._discretization in [self.Discretization.QuadraticExponential,
                                      self.Discretization.QuadraticExponentialMartingale]:
            ex = np.exp(-self._kappa * dt)
            m = self._theta + (x0[1] - self._theta) * ex
            s2 = x0[1] * self._sigma * self._sigma * ex / self._kappa * (1 - ex)
            psi = s2 / (m * m)
            g1 = 0.5
            g2 = 0.5
            k0 = -self._rho * self._kappa * self._theta * dt / self._sigma
            k1 = g1 * dt * (self._kappa * self._rho / self._sigma - 0.5) - self._rho / self._sigma
            k2 = g2 * dt * (self._kappa * self._rho / self._sigma - 0.5) + self._rho / self._sigma
            k3 = g1 * dt * (1 - self._rho * self._rho)
            k4 = g2 * dt * (1 - self._rho * self._rho)
            A = k2 + 0.5 * k4
            if psi < 1.5:
                b2 = 2 / psi - 1 + np.sqrt(2 / psi * (2 / psi - 1))
                b = np.sqrt(b2)
                a = m / (1 + b2)
                if self._discretization == self.Discretization.QuadraticExponentialMartingale:
                    if A >= 1 / (2 * a):
                        raise RuntimeError('illegal value')
                    k0 = -A * b2 * a / (1 - 2 + A * a) + 0.5 * np.log(1 - 2 * A * a) - (k1 + 0.5 * k3) * x0[1]
                retVal[1] = a * (b + dw[1]) * (b + dw[1])
            else:
                p = (psi - 1) / (psi + 1)
                beta = (1 - p) / m
                u = CumulativeNormDistribution()(dw[1])
                if self._discretization == self.Discretization.QuadraticExponentialMartingale:
                    if A >= beta:
                        raise RuntimeError('illegal value')
                    k0 = -np.log(p + beta * (1 - p) / (beta - A)) - (k1 + 0.5 * k3) * x0[1]
                    retVal[1] = 0 if u <= p else np.log((1 - p) / (1 - u) / beta)
            mu = self._riskFreeRate.forwardRate(t0, t0 + dt, Compounding.Continuous) - self._dividendYield.forwardRate(
                t0, t0 + dt, Compounding.Continuous)
            retVal[0] = x0[0] * np.exp(
                mu * dt + k0 + k1 * x0[1] + k2 * retVal[1] + np.sqrt(k3 * x0[1] + k4 * retVal[1]) * dw[0])
        elif self._discretization in [self.Discretization.BroadieKayaExactSchemeLobatto,
                                      self.Discretization.BroadieKayaExactSchemeLaguerre,
                                      self.Discretization.BroadieKayaExactSchemeTrapezoidal]:
            nu_0 = x0[1]
            nu_t = varianceDistribution(nu_0, dw[1], dt)
            x = min(1 - 10 ^ -9, max(0, CumulativeNormDistribution()(dw[2])))
            vds = Brent().solve(bind(cdf_nu_ds_minus_x, self, _1, nu_0, nu_t, dt, self._discretization, x), 10 ^ -5,
                                self._theta * dt, 0.1 * self._theta * dt)
            vdw = (nu_t - nu_0 - self._kappa * self._theta * dt + self._kappa * vds) / self._sigma
            mu = (self._riskFreeRate.forwardRate(t0, t0 + dt, Compounding.Continuous) - self._dividendYield.forwardRate(
                t0, t0 + dt, Compounding.Continuous)) * dt - 0.5 * vds + self._rho * vdw
            sig=np.sqrt((1-self._rho*self._rho)*vds)
            s=x0[0]*np.exp(mu+sig*dw[0])
            retVal[0]=s
            retVal[1]=nu_t
        else:
            raise RuntimeError('unknown discretization schema')
        return retVal

    def v0(self):
        return self._v0

    def rho(self):
        return self._rho

    def kappa(self):
        return self._kappa

    def theta(self):
        return self._theta

    def sigma(self):
        return self._sigma

    def s0(self):
        return self._s0

    def dividendYield(self):
        return self._dividendYield

    def riskFreeRate(self):
        return self._riskFreeRate

    def time(self, d):
        return self._riskFreeRate.datCounter().yearFraction(self._riskFreeRate.referenceDate(), d)

    def pdf(self, x, v, t, eps=10 ^ -3):
        k = self._sigma * self._sigma * (1 - np.exp(-self._kappa * t)) / (4 * self._kappa)
        a = np.log(self._dividendYield.discount(t) / self._riskFreeRate.discount(t)) + self._rho / self._sigma * (
                v - self._v0 - self._kappa * self._theta * t)
        x0 = np.log(self._s0.value)
        upper = max(0.1, -(x - x0 - a) / (0.5 - self._rho * self._kappa / self._sigma))
        f = 0
        df = 1
        while (df > 0 or f > 0.1 * eps):
            f1 = x - x0 - a + upper * (0.5 - self._rho * self._kappa / self._sigma)
            f2 = -0.5 * f1 * f1 / (upper * (1 - self._rho * self._rho))
            df = 1 / np.sqrt(2 * math.pi * (1 - self._rho * self._rho)) * (
                    -0.5 / (upper * np.sqrt(upper)) * np.exp(f2) + 1 / np.sqrt(upper) * np.exp(f2) * (
                    -0.5 / (1 - self._rho * self._rho)) * (-1 / (upper * upper) * f1 * f1 + 2 / upper * f1 * (
                    0.5 - self._rho * self._kappa / self._sigma)))
            f = np.exp(f2) / np.sqrt(2 * math.pi * (1 - self._rho * self._rho) * upper)
            upper = 1.5
        upper = 2 * cornishFisherEps(self, self._v0, v, t, 10 ^ -3)
        return SegmentIntegral(100)(bind(int_ph, self, a, x, _1, self._v0, v, t), 10 ^ -9, upper) * pdf(
            non_central_chi_squared_distribution(4 * self._theta * self._kappa / (self._sigma * self._sigma),
                                                 4 * self._kappa * np.exp(-self._kappa * t) / (
                                                         (self._sigma * self._sigma) * (
                                                         1 - np.exp(-self._kappa * t))) * self._v0), v / k) / k

    def varienceDistribution(self, v, dw, dt):
        df = 4 * self._theta * self._kappa / (self._sigma * self._sigma)
        ncp = 4 * self._kappa * np.exp(-self._kappa * dt) / (
                self._sigma * self._sigma * (1 - np.exp(-self._kappa * dt))) * v
        p = min(1 - 10 ^ -9, max(0, CumulativeNormDistribution()(dw)))
        return self._sigma * self._sigma * (1 - np.exp(-self._kappa * dt)) / (
                4 * self._kappa) * InverseNoncentralCumulativeChiSquareDistribution(df, ncp, 100)(p)
