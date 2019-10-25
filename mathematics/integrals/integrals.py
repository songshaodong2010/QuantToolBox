class Integrator:
    def __init__(self, absoluteAccuracy, maxEvaluations):
        self._absoluteAccuracy = absoluteAccuracy
        self._maxEvaluations = maxEvaluations
        self._absoluteError = None
        self._evalustions = None
        if absoluteAccuracy <= 10 ^ -9:
            raise RuntimeError('required tolerance not allowed. It must be > 10^-9')

    def __call__(self, f, a, b):
        self._evaluations=0
        if a==b:
            return 0
        if b>a:
            return self.integrate(f,a,b)
        else:
            return -self.integrate(f,b,a)

    def setAbsoluteAcuracy(self, accuracy):
        self._absoluteAccuracy = accuracy

    def setMaxEvaluations(self, maxEvaluations):
        self._maxEvaluations = maxEvaluations

    def absoluteAccuracy(self):
        return self._absoluteAccuracy

    def maxEvaluations(self):
        return self._maxEvaluations

    def absoluteError(self):
        return self._absoluteError

    def setAbsoluteError(self, error):
        self._absoluteError = error

    def numberOfEvaluations(self):
        return self._evalustions

    def setNumberOfEvaluations(self, evaluations):
        self._evaluations = evaluations

    def integrationSuccess(self):
        return self._evalustions <= self._maxEvaluations and self._absoluteError <= self._absoluteAccuracy

    def increaseNumberOfEvaluations(self, increase):
        self._evalustions += increase

    def integrate(self,f,a,b):
        pass
