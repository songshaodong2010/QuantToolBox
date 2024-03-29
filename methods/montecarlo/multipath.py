from methods.montecarlo.path import Path


class MultiPath:
    def __init__(self, nAsset=None, timeGrid=None, multiPath=None):
        if nAsset is not None and timeGrid is not None and multiPath is None:
            self._multiPath = [Path(timeGrid) for i in range(nAsset)]
        elif nAsset is None and timeGrid is None and multiPath is not None:
            self._multiPath = multiPath
        else:
            raise RuntimeError('wrong parameter')

    def assetNumber(self):
        return self._multiPath.size()

    def pathSize(self):
        return len(self._multiPath[0])

    def __getitem__(self, item):
        return self._multiPath[item]
