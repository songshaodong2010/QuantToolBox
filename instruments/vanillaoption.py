from instruments.oneassetoption import *

'''
检查完毕，impliedVolatility需要补充
'''


class VanillaOption(OneAssetOption):
    def __init__(self, payoff, exercise):
        OneAssetOption.__init__(self, payoff, exercise)

    def impliedVolatility(self, targetValue, process, accuracy=10 ** -4, maxEvaluations=100, minVol=10 ** -7,
                          maxVol=4.0):
        pass
