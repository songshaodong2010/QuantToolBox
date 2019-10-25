from grid import *
from methods.montecarlo.montecarlomodel import *


class McSimulation:
    def __init__(self, antitheticVariate, controlVariate,mcModel=None):
        self._antitheticVariate = antitheticVariate
        self._controlVariate = controlVariate
        self._mcModel = mcModel

    def value(self, tolerance, maxSamples=999999999, minSamples=1023):
        sampleNumber = self._mcModel.sampleAccumulator().samples()
        if sampleNumber < minSamples:
            self._mcModel.addSamples(minSamples - sampleNumber)
            sampleNumber = self._mcModel.sampleAccumulator().samples()
        nextBatch = None
        order = None
        error = self._mcModel.sampleAccumulator().errorEstimate()
        while self.maxError(error) > tolerance:
            if sampleNumber >= maxSamples:
                raise RuntimeError('max number of samples reached, while error is still above tolerance')
            order = self.maxError(error * error) / tolerance / tolerance
            nextBatch = int(max(sampleNumber * order * 0.8 - sampleNumber, minSamples))
            nextBatch = min(nextBatch, maxSamples - sampleNumber)
            sampleNumber += nextBatch
            self._mcModel.addSamples(nextBatch)
            error = self._mcModel.sampleAccumulator().errorEstimate()
        return self._mcModel.sampleAccumulator().mean()

    def valueWithSamples(self, samples):
        samplesNumber = self._mcModel.sampleAccumulator().samples()
        if samples < samplesNumber:
            raise RuntimeError('number of already simulated samples greater than requested samples')
        self._mcModel.addSamples(samples - samplesNumber)
        return self._mcModel.sampleAccumulator().mean()

    def errorEstimate(self):
        return self._mcModel.sampleAccumulator().errorEstimate()

    def sampleAccumulator(self):
        return self._mcModel.sampleAccumulator()

    def calculate(self, requiredTolerance, requiredSamples, maxSample=None):
        if requiredTolerance is None or requiredSamples is None:
            raise RuntimeError('neither tolerance nor number of samples set')
        if self._controlVariate:
            controlVariateValue = self.controlVariateValue()
            if controlVariateValue is None:
                raise RuntimeError('engine does not provide control-variation price')
            controlPP = self.controlPathPricer()
            if controlPP is None:
                raise RuntimeError('engine does not provide control-variation price')
            controlPG = self.controlPathGenerator()
            self._mcModel = MonteCarloModel(self.pathGenerator(), self.pathPricer(), None,
                                            self._antitheticVariate, cvPathPricer=controlPP,
                                            cvOptionValue=controlVariateValue, cvPathGenerator=controlPG)
        else:
            self._mcModel = MonteCarloModel(self.pathGenerator(), self.pathPricer(), None, self._antitheticVariate)
        if requiredTolerance is not None:
            if maxSample is not None:
                self.value(requiredTolerance, maxSamples=maxSample)
            else:
                self.value(requiredTolerance)
        else:
            self.valueWithSamples(requiredSamples)

    def pathPricer(self):
        pass

    def pathGenerator(self):
        pass

    def timeGrid(self):
        pass

    def controlPathPricer(self):
        return None

    def controlPricingEngine(self):
        return None

    def controlVariateValue(self):
        return None

    def controlPathGenerator(self):
        return None

    def maxError(self, sequence):
        if isinstance(sequence, list):
            return max(sequence)
        else:
            return sequence
