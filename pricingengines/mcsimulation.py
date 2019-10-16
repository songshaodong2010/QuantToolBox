from grid import *
from methods.montecarlo.montecarlomodel import *

class McSimulation:
    def value(self,tolerance,maxSamples=999999999,minSample=1023):
        pass

    def valueWithSamples(self,samples):
        pass

    def errorEstimate(self):
        pass

    def sampleAccumulator(self):
        pass

    def calculate(self,requiredTolerance,requiredSamples,maxSample):
        pass

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

    def maxError(self,sequence=None,error=None):
        if sequence is not None and error is None:
            return max_element(sequence.begin(),sequence.end())
        elif sequence is None and error is not None:
            return error
