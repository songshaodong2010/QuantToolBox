from methods.montecarlo.path import Path

class MultiPath:
    def __init__(self,nAsset=None,timeGrid=None,multiPath=None):
        if nAsset is not None and timeGrid is not None and multiPath is None:
            self._multiPath = (nAsset,timeGrid)
        elif nAsset is None and timeGrid is None and multiPath is not None:
            self._multiPath = multiPath
        else:
            raise RuntimeError('wrong parameter')

    def assetNumber(self):
        return self._multiPath.size()

    def pathSize(self):
        return len(self._multiPath[0])

    def operator(self,j):
        return self._multiPath[j]

    def at(self,j):
        return self._multiPath.at(j)
