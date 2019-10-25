from instruments.vanillaoption import *
from pricingengines.mcsimulation import *
from timegrid import *
from methods.montecarlo.pathgenerator import *


class MCVanillaEngine(VanillaOption.engine, McSimulation):
    def __init__(self, process, timeSteps, timeStepPerYear, brownianBridge, antitheticVariate, controlVariate,
                 requiredSamples, requiredTolerance, maxSamples, seed):
        McSimulation.__init__(self, antitheticVariate, controlVariate)
        self._process = process
        self._timeSteps = timeSteps
        self._timeStepsPerYear = timeStepPerYear
        self._requiredSamples = requiredSamples
        self._maxSample = maxSamples
        self._requiredTolerance = requiredTolerance
        self._brownianBridge = brownianBridge
        self._seed = seed
        if timeSteps is None and timeStepPerYear is None:
            raise RuntimeError('no time steps provided')
        if timeSteps is not None and timeStepPerYear is not None:
            raise RuntimeError('both time steps and time steps per year were provided')
        if timeSteps <= 0:
            raise RuntimeError('timeSteps must be positive')
        if timeStepPerYear <= 0:
            raise RuntimeError('timeStepPerYear must be positive')
        self.registerWith(self._process)

    def calculate(self):
        McSimulation.calculate(self, self._requiredTolerance, self._requiredSamples, maxSample=self._maxSample)
        self._results.value = self._mcModel.sampleAccumulator().mean()
        # if RNG.allowsEstimate:
        self._results.errorEstimate = self._mcModel.sampleAccumulator().errorEstimate()

    def timeGrid(self):
        lastExerciseDate = self._arguments._exercise.lastDate()
        t = self._process.time(lastExerciseDate)
        if self._timeSteps is not None:
            return TimeGrid(end=t, steps=self._timeSteps)
        elif self._timeStepsPerYear is not None:
            steps = self._timeStepsPerYear * t
            return TimeGrid(end=t, steps=max(steps, 1))
        else:
            raise RuntimeError('time steps not specified')

    def pathGenerator(self):
        dimensions = self._process.factors()
        grid = self.timeGrid()
        generator = RNG.make_sequence_generator(dimensions * (grid.size() - 1), self._seed)
        return PathGenerator(self._process, generator, self._brownianBridge, timeGrid=grid)

    def controlVariateValue(self):
        controlPE = self.controlPricingEngine()
        if controlPE is None:
            raise RuntimeError('engine does not provide control variation pricing engine')
        controlArguments = controlPE.getArguments()
        if controlArguments is None:
            raise RuntimeError('engine is using inconsistent arguments')
        controlArguments = self._arguments
        controlPE.calculate()
        controlResults = controlPE.getResults()
        if controlResults is None:
            raise RuntimeError('engine returns an inconsistent result type')
        return controlResults.value
