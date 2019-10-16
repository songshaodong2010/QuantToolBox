class TimeGrid:
    def __init__(self, begin=None, end=None, steps=None):
        if begin is None and end is not None and steps is not None:
            if end <= 0:
                raise RuntimeError('negative times not allowed')
            dt = end / steps
            self._times.reserve(steps + 1)
            for i in range(steps + 1):
                self._times.push_back(dt * i)
            self._mandatoryTimes = [end]
            self._dt = [dt for i in range(steps)]
        elif begin is not None and end is not None and steps is None:
            self._mandatoryTimes = [begin, end]
            if begin is end:
                raise RuntimeError('empty time sequence')
            sorted(self._mandatoryTimes)
            if self._mandatoryTimes.front() < 0:
                raise RuntimeError('negative times not allowed')
            self._mandatoryTimes.resize(self._mandatoryTimes - self._mandatoryTimes.begin())
            last = self._mandatoryTimes.back()
            dtMax = None
            if steps == 0:
                diff = None
                adjacent_difference(self.begin)

        self._times = None
        self._dt = None
        self._mandatoryTimes = None

    def __getitem__(self, item):
        return self._times[item]

    def size(self):
        return self._times.size()

    def empty(self):
        return self._times is None

    def front(self):
        return self._times.front()

    def back(self):
        return self._times.back()
