import numpy as np
import math


class I:
    def value(self):
        return 0


class Unweighted:
    def weightSmallX(self, x):
        return 1

    def weightLargeX(self, x):
        return np.exp(x)

    def weight2LargeX(self, x):
        return np.exp(-x)


class ExponentiallyWeighted:
    def weightSmallX(self, x):
        return np.exp(-x)

    def weightLargeX(self, x):
        return 1

    def weight2LargeX(self, x):
        return np.exp(-2 * x)


def modifiedBesselFunction_i_impl(nu, x, W=Unweighted):
    if abs(x) < 13:
        alpha = np.power(0.5 * x, nu) / GammaFunction().value(1 + nu)
        Y = 0.25 * x * x
        k = 1
        sum = alpha
        B_k = alpha
        B_k *= Y / (k * (k + nu))
        while abs(B_k) > abs(sum) * 10 ^ -9:
            sum += B_k
            k += 1
            if k >= 1000:
                raise RuntimeError('max iterations exceeded')
            B_k *= Y / (k * (k + nu))
        return sum * W().weightSmallX(x)
    else:
        na_k = 1
        sign = 1
        da_k = 1
        s1 = 1
        s2 = 1
        for k in range(1, 30):
            sign *= -1
            na_k *= (4 * nu * nu - (2 * k - 1) * (2 * k - 1))
            da_k *= (8 * k) * x
            a_k = na_k / da_k
            s2 += a_k
            s1 += sign * a_k
        i = I().value()
        return 1 / np.sqrt(2 * math.pi * x) * (W().weightLargeX(x) * s1 + i * np.exp(
            i * nu * math.pi) * W().weight2LargeX(x) * s2)


def modifiedBesselFunction_k_impl(nu, x, W=Unweighted):
    return math.pi / 2 * (
                modifiedBesselFunction_i_impl(-nu, x, W=W) - modifiedBesselFunction_i_impl(nu, x, W=W)) / np.sin(
        math.pi * nu)


def modifiedBesselFunction_i(nu, x):
    if x < 0:
        raise RuntimeError('negative argument requires complex version of modifiedBesselFunction')
    return modifiedBesselFunction_i_impl(nu, x)


def modifiedBesselFunction_k(nu, x):
    if x < 0:
        raise RuntimeError('negative argument requires complex version of modifiedBesselFunction')
    return modifiedBesselFunction_k_impl(nu, x)


def modifiedBesselFunction_i_exponentiallyWeight(nu, x):
    if x < 0:
        raise RuntimeError('negative argument requires complex version of modifiedBesselFunction')
    return modifiedBesselFunction_i_impl(nu, x,W=ExponentiallyWeighted)


def modifiedBesselFunction_k_exponentiallyWeight(nu, x):
    if x < 0:
        raise RuntimeError('negative argument requires complex version of modifiedBesselFunction')
    return modifiedBesselFunction_k_impl(nu, x,W=ExponentiallyWeighted)
