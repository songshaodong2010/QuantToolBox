from instruments.vanillaoption import *

'''
检查完毕，无需修改
'''


class EuropeanOption(VanillaOption):
    def __init__(self, payoff, exercise):
        VanillaOption.__init__(self, payoff, exercise)
