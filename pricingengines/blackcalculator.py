import numpy as np
import scipy.stats as sps
from instruments.payoffs import *


class BlackCalculator():
    def __init__(self, p, forward, stdDev, discount=1.0):
        self._strike = p.strike()
        self._forward = forward
        self._stdDev = stdDev
        self._discount = discount
        self._variance = stdDev * stdDev
        self._d1 = None
        self._d2 = None
        self._alpha = None
        self._beta = None
        self._DalphaD1 = None
        self._DbetaD2 = None
        self._n_d1 = None
        self._n_d2 = None
        self._cum_d1 = None
        self._cum_d2 = None
        self._x = None
        self._DxDs = None
        self._DxDstrike = None
        self.initialize(p)

    def initialize(self, p):
        if self._strike < 0:
            raise RuntimeError('strike must be non-negative')
        if self._forward <= 0:
            raise RuntimeError('forward must be positive')
        if self._stdDev < 0:
            raise RuntimeError('stdDev must be non-negative')
        if self._discount <= 0:
            raise RuntimeError('discount must be positive')
        self._d1 = np.log(self._forward / self._strike) / self._stdDev + 0.5 * self._stdDev
        self._d2 = self._d1 - self._stdDev
        self._cum_d1 = sps.norm.cdf(self._d1)
        self._cum_d2 = sps.norm.cdf(self._d2)
        self._n_d1 = sps.norm.pdf(self._d1)
        self._n_d2 = sps.norm.pdf(self._d2)
        self._x = self._strike
        self._DxDs = 0.0
        self._DxDstrike = 1.0
        if p.optionType().name == 'Call':
            self._alpha = self._cum_d1
            self._DalphaD1 = self._n_d1
            self._beta = -self._cum_d2
            self._DbetaD2 = -self._n_d2
        elif p.optionType().name == 'Put':
            self._alpha = -1.0 + self._cum_d1
            self._DalphaD1 = self._n_d1
            self._beta = 1.0 - self._cum_d2
            self._DbetaD2 = -self._n_d2
        else:
            raise RuntimeError('invalid option type')
        if isinstance(p, CashOrNothingPayoff):
            self._alpha = self._DalphaD1 = 0.0
            self._x = p.cashPayoff()
            self._DxDstrike = 0.0
            if p.optionType().name == 'Call':
                self._beta = self._cum_d2
                self._DbetaD2 = self._n_d2
            elif p.optionType().name == 'Put':
                self._beta = 1.0 - self._cum_d2
                self._DbetaD2 = -self._n_d2
            else:
                raise RuntimeError('invalid option type')
        if isinstance(p, AssetOrNothingPayoff):
            self._beta = self._DbetaD2 = 0.0
            if p.optionType().name == 'Call':
                self._alpha = self._cum_d1
                self._DalphaD1 = self._n_d1
            elif p.optionType().name == 'Put':
                self._alpha = 1.0 - self._cum_d1
                self._DalphaD1 = -self._n_d1
            else:
                raise RuntimeError('invalid option type')
        if isinstance(p, GapPayoff):
            self._x = p.secondStrike()
            self._DxDstrike = 0

    def value(self):
        result = self._discount * (self._forward * self._alpha + self._x * self._beta)
        return result

    def delta(self, spot):
        if spot <= 0:
            raise RuntimeError('spot must be positive')
        DforwardDs = self._forward / spot
        temp = self._stdDev * spot
        DalphaDs = self._DalphaD1 / temp
        DbetaDs = self._DbetaD2 / temp
        temp2 = DalphaDs * self._forward + self._alpha * DforwardDs + DbetaDs * self._x + self._beta * self._DxDs
        return self._discount * temp2

    def gamma(self, spot):
        if spot <= 0:
            raise RuntimeError('spot must be positive')
        DforwardDs = self._forward / spot
        temp = self._stdDev * spot
        DalphaDs = self._DalphaD1 / temp
        DbetaDs = self._DbetaD2 / temp
        D2alphaDs2 = -DalphaDs * spot * (1 + self._d1 / self._stdDev)
        D2betaDs2 = -DbetaDs * spot * (1 + self._d2 / self._stdDev)
        temp2 = D2alphaDs2 * self._forward + 2.0 * DalphaDs * DforwardDs + D2betaDs2 * self._x + 2.0 * DbetaDs * self._DxDs
        return self._discount * temp2

    def theta(self, spot, maturity):
        if maturity < 0:
            raise RuntimeError('maturity must be non-negative')
        return -(np.log(self._discount) * self.value() + np.log(self._forward / spot) * spot * self.delta(
            spot) + 0.5 * self._variance * spot * spot * self.gamma(spot)) / maturity

    def vega(self, maturity):
        if maturity < 0:
            raise RuntimeError('maturity must be non-negative')
        temp = np.log(self._strike / self._forward) / self._variance
        DalphaDsigma = self._DalphaD1 * (temp + 0.5)
        DbetaDsigma = self._DbetaD2 * (temp - 0.5)
        temp2 = DalphaDsigma * self._forward + DbetaDsigma * self._x
        return self._discount * np.sqrt(maturity) * temp2

    def rho(self, maturity):
        if maturity < 0:
            raise RuntimeError('maturity must be non-negative')
        DalphaDr = self._DalphaD1 / self._stdDev
        DbetaDr = self._DbetaD2 / self._stdDev
        temp = DalphaDr * self._forward + self._alpha * self._forward + DbetaDr * self._x
        return maturity * (self._discount * temp - self.value())
