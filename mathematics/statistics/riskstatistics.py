import numpy as np


class GenericRiskStatistics:
    def __init__(self, s_type):
        self.s_type = s_type

    def semiVariance(self):
        return self.regret(self.mean())

    def semiDeviation(self):
        return np.sqrt(self.semiVariance())

    def downsideVariance(self):
        return self.regret(0)

    def downsideDeviation(self):
        return np.sqrt(self.downsideVariance())

    def regret(self, target):
        result = self.expectationValue(compose(None, target), target)
        x = result.first
        N = result.secend
        if N <= 1:
            raise RuntimeError('samples under target <= 1, unsufficient')
        return (N / (N - 1)) * x

    def potentialUpdate(self, percentile):
        if percentile < 0.9 or percentile >= 1:
            raise RuntimeError('percentile out of range [0.9, 1.0)')
        return max(self.percentile(percentile), 0)

    def valueAtRisk(self, percentile):
        if percentile < 0.9 or percentile >= 1:
            raise RuntimeError('percentile out of range [0.9, 1.0)')
        return min(self.percentile(1 - percentile), 0)

    def expectedShortfall(self, percentile):
        if percentile < 0.9 or percentile >= 1:
            raise RuntimeError('percentile out of range [0.9, 1.0)')
        if self.samples() == 0:
            raise RuntimeError('empty sample set')
        target = -self.valueAtRisk(percentile)
        result = self.expectationValue(None, target)
        x = result.first
        N = result.secend
        if N == 0:
            raise RuntimeError('no data below the target')
        return -min(x, 0)

    def shortfall(self, target):
        if self.samples() == 0:
            raise RuntimeError('empty sample set')
        return self.expectationValue(clip(1,target),everywhere()).first

    def averageShortfall(self, target):
        result=self.expectationValue(target,target)
        x=result.first
        N=result.secend
        if N == 0:
            raise RuntimeError('no data below the target')
        return x


class RiskStatistics(GenericRiskStatistics):
    def __init__(self):
        GenericRiskStatistics.__init__(self, GaussianStatistics)
