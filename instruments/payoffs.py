from payoff import *
from option import *

'''
检查完毕，不用访问者模式了
'''

class NullPayoff(Payoff):
    def name(self):
        return 'Null'

    def description(self):
        return self.name()

    def __call__(self, price):
        raise RuntimeError('dummy payoff given')


class TypePayoff(Payoff):
    def __init__(self, type):
        self._type = type

    def optionType(self):
        return self._type

    def name(self):
        return self.optionType().name

    def description(self):
        result = 'OptionType:' + self.name()
        return result


class FloatingTypePayoff(TypePayoff):
    def __init__(self, type):
        TypePayoff.__init__(self, type)

    def name(self):
        return 'FloatingType'

    def description(self):
        result = 'OptionType:' + self.name()
        return result

    def __call__(self, price):
        raise RuntimeError('"floating payoff not handled"')


class StrikedTypePayoff(TypePayoff):
    def __init__(self, type, strike):
        TypePayoff.__init__(self, type)
        self._strike = strike

    def strike(self):
        return self._strike

    def description(self):
        result = TypePayoff.description(self)
        result += ',Strike:' + str(self.strike())
        return result


class PlainVanillaPayoff(StrikedTypePayoff):
    def __init__(self, type, strike):
        StrikedTypePayoff.__init__(self, type, strike)

    def name(self):
        return 'Vanilla'

    def __call__(self, price):
        if self._type.name == 'Call':
            return max(price - self._strike, 0.0)
        elif self._type.name == 'Put':
            return max(self._strike - price, 0.0)
        else:
            raise RuntimeError('unknown/illegal option type')


class PercentageStrikePayoff(StrikedTypePayoff):
    def __init__(self, type, moneyness):
        StrikedTypePayoff.__init__(self, type, moneyness)

    def name(self):
        return 'PercentageStrike'

    def __call__(self, price):
        if self._type.name == 'Call':
            return price * max(1.0 - self._strike, 0)
        elif self._type.name == 'Put':
            return price * max(self._strike - 1.0, 0)
        else:
            raise RuntimeError('unknown/illegal option type')


class AssetOrNothingPayoff(StrikedTypePayoff):
    def __init__(self, type, strike):
        StrikedTypePayoff.__init__(self, type, strike)

    def name(self):
        return 'AssetOrNothing'

    def __call__(self, price):
        if self._type.name == 'Call':
            return price if price > self._strike else 0
        elif self._type.name == 'Put':
            return price if price < self._strike else 0
        else:
            raise RuntimeError('unknown/illegal option type')


class CashOrNothingPayoff(StrikedTypePayoff):
    def __init__(self, type, strike, cashPayoff):
        StrikedTypePayoff.__init__(self, type, strike)
        self._cashPayoff = cashPayoff

    def name(self):
        return 'CashOrNothing'

    def __call__(self, price):
        if self._type.name == 'Call':
            return self._cashPayoff if price > self._strike else 0
        elif self._type.name == 'Put':
            return self._cashPayoff if price < self._strike else 0
        else:
            raise RuntimeError('unknown/illegal option type')

    def cashPayoff(self):
        return self._cashPayoff


class GapPayoff(StrikedTypePayoff):
    def __init__(self, type, strike, secondStrike):
        StrikedTypePayoff.__init__(self, type, strike)
        self._secondStrike = secondStrike

    def name(self):
        return 'Gap'

    def secondStrike(self):
        return self._secondStrike

    def description(self):
        result = super().description()
        result += ',SecondStrike:' + str(self.secondStrike())
        return result

    def __call__(self, price):
        if self._type.name == 'Call':
            return price - self._secondStrike if price >= self._strike else 0
        elif self._type.name == 'Put':
            return self._secondStrike - price if price <= self._strike else 0
        else:
            raise RuntimeError('unknown/illegal option type')
