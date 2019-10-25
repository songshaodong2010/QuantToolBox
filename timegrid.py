class TimeGrid:
    def __init__(self, points=None, end=None, steps=None):
        self._times = []
        self._dt = []
        self._mandatoryTimes = []
        if points is None and end is not None and steps is not None:
            if end <= 0:
                raise RuntimeError('negative times not allowed')
            dt = end / steps
            for i in range(steps + 1):
                self._times.append(dt * i)
            self._mandatoryTimes.append(end)
            self._dt = [dt for i in range(steps)]
        elif points is not None and end is None and steps is None:
            self._mandatoryTimes = points
            if len(points) <= 1:
                raise RuntimeError('empty time sequence')
            self._mandatoryTimes.sort()
            if self._mandatoryTimes[0] < 0:
                raise RuntimeError('negative times not allowed')
            e = []
            [e.append(item) for item in self._mandatoryTimes if not item in e]
            self._mandatoryTimes = [item - self._mandatoryTimes[0] for item in self._mandatoryTimes]
            if self._mandatoryTimes[0] > 0:
                self._times.append(0)
            self._times.extend(self._mandatoryTimes)
            self._dt = [self._times[i + 1] - self._times[i] for i in range(len(self._times) - 1)]
        elif points is not None and end is None and steps is not None:
            self._mandatoryTimes = points
            if len(points) <= 1:
                raise RuntimeError('empty time sequence')
            self._mandatoryTimes.sort()
            if self._mandatoryTimes[0] < 0:
                raise RuntimeError('negative times not allowed')
            e = []
            [e.append(item) for item in self._mandatoryTimes if not item in e]
            self._mandatoryTimes = [item - self._mandatoryTimes[0] for item in self._mandatoryTimes]
            last = self._mandatoryTimes[-1]
            if steps == 0:
                diff = [self._mandatoryTimes[0]]
                diff.extend([self._mandatoryTimes[i + 1] - self._mandatoryTimes[i] for i in
                             range(len(self._mandatoryTimes) - 1)])
                if diff[0] == 0:
                    diff.pop(0)
                dtMax = min(diff)
            else:
                dtMax = last / steps
            periodBegin = 0
            self._times.append(periodBegin)
            for t in self._mandatoryTimes:
                periodEnd = t
                if periodEnd != 0:
                    nSteps = int((periodEnd - periodBegin) / dtMax + 0.5)
                    nSteps = nSteps if nSteps != 0 else 1
                    dt = (periodEnd - periodBegin) / nSteps
                    self._times = [(i + 1) * dt for i in range(nSteps)]
                periodBegin = periodEnd
            self._dt = [self._times[i + 1] - self._times[i] for i in range(len(self._times) - 1)]
        else:
            raise RuntimeError('Wrong parameter!')

    def __getitem__(self, item):
        return self._times[item]

    def size(self):
        return len(self._times)

    def empty(self):
        return len(self._times) == 0

    def dt(self, i):
        return self._dt[i]
