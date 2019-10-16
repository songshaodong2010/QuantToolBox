from instruments.europeanoption import *
from pricingengines.vanilla.analyticeuropeanengine import *
from processes.blackscholesprocess import *
from termstructures.yields.flatforward import *
from timecustomized.calendars.china import *
from termstructures.volatility.equityfx.blackconstantvol import *
from pricingengines.blackcalculator import *
import datetime

type = Option.Type.Put
strike = 40
underlying = 36
underlyingH = SimpleQuote(underlying)
dividendYield = 0.00
riskFreeRate = 0.06
volatility = 0.20
maturity = datetime.date(1999, 5, 17)
todayDate = datetime.date(1998, 5, 17)
settlementDate = datetime.date(1998, 5, 17)
dayCounter = Actual365()
calendar_option = China()
Settings().setEvaluationDate(todayDate)
flatTermStructure = FlatForward(riskFreeRate, dayCounter, referenceDate=settlementDate, cal=calendar_option)
flatDividendTS = FlatForward(dividendYield, dayCounter, referenceDate=settlementDate, cal=calendar_option)
flatVolTS = BlackConstantVol(volatility, dayCounter, calendar_option, referenceDate=settlementDate)
europeanExercise = EuropeanExercise(maturity)
EurPayoff = PlainVanillaPayoff(type, strike)
process = BlackscholesMertonProcess(underlyingH, flatDividendTS, flatTermStructure, flatVolTS)
engine = AnalyticEuropeanEngine(process)
va = EuropeanOption(EurPayoff, europeanExercise)
va.setPricingEngine(engine)
print(va.NPV())
print('hello world')
