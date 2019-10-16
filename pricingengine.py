from patterns.observable import *

'''
检查完毕，无需修改
'''


class PricingEngine(Observable):
    def __init__(self):
        Observable.__init__(self)

    def getArguments(self):
        pass

    def getResults(self):
        pass

    def reset(self):
        pass

    def calculate(self):
        pass

    class arguments:
        def validate(self):
            pass

    class results:
        def reset(self):
            pass


class GenericEngine(PricingEngine, Observer):
    def __init__(self):
        PricingEngine.__init__(self)
        Observer.__init__(self)
        self._arguments = PricingEngine.arguments()
        self._results = PricingEngine.results()

    def getArguments(self):
        return self._arguments

    def getResults(self):
        return self._results

    def reset(self):
        self._results.reset()

    def update(self):
        self.notifyObservers()
