class Extropolator:#插值抽象类
    def __init__(self):
        self._extrapolate = False

    def enableExtrapolation(self, b=True):
        self._extrapolate = b

    def disableExtrapolation(self, b=True):
        self._extrapolate = (not b)

    def allowsExtrapolation(self):
        return self._extrapolate