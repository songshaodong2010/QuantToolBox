from pricingengines.vanilla.mcvanillaengine import *
from processes.blackscholesprocess import *
from termstructures.volatility.equityfx.blackconstantvol import *
from termstructures.volatility.equityfx.blackvariancecurve import *
from methods.montecarlo.pathpricer import *
from instruments.payoffs import *


class MCEuropeanEngine(MCVanillaEngine):
    def __init__(self, process, timeSteps, timeStepsPerYear, brownianBridge, antitheticVariate, requiredSamples,
                 requiredTorance, maxSamples, seed):
        MCVanillaEngine.__init__(self, process, timeSteps, timeStepsPerYear, brownianBridge, antitheticVariate, False,
                                 requiredSamples, requiredTorance, maxSamples, seed)

    def pathPricer(self):
        payoff = self._arguments.payoff
        if payoff is None:
            raise RuntimeError('non-plain payoff given')
        process = self._process
        if process is None:
            raise RuntimeError('Black-Scholes process required')
        return EuropeanPathPricer(payoff.optionType(), payoff.srtike(),
                                  process.riskFreeRate().discount(self.timeGrid()[-1]))


class MakeMCEuropeanEngine:
    def __init__(self, process):
        self._process = process
        self._antithetic = False
        self._steps = None
        self._stepsPerYear = None
        self._samples = None
        self._maxSamples = None
        self._tolerance = None
        self._brownianBridge = False
        self._seed = 0

    def withSteps(self, steps):
        self._steps = steps
        return self

    def withStepsPErYear(self, steps):
        pass

    def withBrownianBridge(self, b=True):
        self._brownianBridge = b
        return self

    def withSamples(self, samples):
        if self._tolerance is not None:
            raise RuntimeError('tolerance already set')
        self._samples = samples
        return self

    def withAbsoluteTolerance(self, tolerance):
        if self._samples is not None:
            raise RuntimeError('number of samples already set')
        if not RNG.allowsErrorEstimate:
            raise RuntimeError('chosen random generator policy does not allow an error estimate')
        self._tolerance = tolerance
        return self

    def withMaxSamples(self, samples):
        self._maxSamples = samples
        return self

    def withSeed(self, seed):
        self._seed = seed
        return self

    def withAntitheticVariate(self, b=True):
        self._antithetic = b
        return self

    def __call__(self):
        if self._steps is None and self._stepsPerYear is None:
            raise RuntimeError('number of steps not given')
        if self._steps is not None and self._stepsPerYear is not None:
            raise RuntimeError('number of steps overSpecified')
        return MCEuropeanEngine(self._process, self._steps, self._stepsPerYear, self._brownianBridge, self._antithetic,
                                self._samples, self._tolerance, self._maxSamples, self._seed)


class EuropeanPathPricer(PathPricer):
    def __init__(self, type, strike, discount):
        self._payoff = PlainVanillaPayoff(type, strike)
        self._discount = discount
        if strike <= 0:
            raise RuntimeError('strike less than zero not allowed')

    def __call__(self, path):
        if path.length()<=0:
            raise RuntimeError('the path cannot be empty')
        return self._payoff(path[-1])*self._discount
