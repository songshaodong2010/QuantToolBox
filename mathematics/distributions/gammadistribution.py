import numpy as np
import math

class CumulativeGammaDistribution:
    def __init__(self,a):
        if a<=0:
            raise RuntimeError('invalid parameter for gamma distribution')
        self._a=a

    def __call__(self, x):
        if x <=0:
            return 0
        gln=GammaFunction().logValue(self._a)
        if x<(self._a+1):
            ap=self._a
            delX=1/self._a
            sum=delX
            for n in range(1,101):
                ap+=1
                delX*=x/ap
                sum+=delX
                if abs(delX)<abs(sum)*3.0e-7:
                    return sum*np.exp(-x+self._a*np.log(x)-gln)
        else:
            b=x+1+self._a
            c=999999999
            d=1/b
            h=d
            for n in range(1,101):
                an=-1*n*(n-self._a)
                b+=2
                d=an*d+b
                if abs(d)<10^-9:
                    d=10^-9
                c=b+an/c
                if abs(c)<10^-9:
                    c=10^-9
                d=1/d
                delX=d*c
                h*=delX
                if abs(delX-1)<10^-9:
                    return 1-h*np.exp(-x+self._a*np.log(x)-gln)


class GammaFunction:
    def __init__(self):
        self._c1=76.18009172947146
        self._c2=-86.50532032941677
        self._c3=24.01409824083091
        self._c4=-1.231739572450155
        self._c5=0.001208650973866179
        self._c6=-0.5395239384953e-5

    def value(self,x):
        if x>=1:
            return np.exp(self.logValue(x))
        else:
            if x>-20:
                return self.value(x+1)/x
            else:
                return -math.pi/(self.value(-x)*x*np.sin(math.pi*x))

    def logValue(self,x):
        if x <=0:
            raise RuntimeError('positive argument required')
        temp=x+5.5
        temp-=(x+0.5)*np.log(temp)
        ser=1.000000000190015
        ser += self._c1/(x + 1.0)
        ser += self._c2/(x + 2.0)
        ser += self._c3/(x + 3.0)
        ser += self._c4/(x + 4.0)
        ser += self._c5/(x + 5.0)
        ser += self._c6/(x + 6.0)
        return -temp+np.log(2.5066282746310005*ser/x)


