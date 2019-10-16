import numpy as np
def CenteredGrid(center, dx, steps):
    result = []
    for i in range(steps + 1):
        result[i] = center + (i - steps / 2) * dx
    return result


def BoundedGrid(xMin, xMax, steps):
    result = []
    x = xMin
    dx = (xMax - xMin) / steps
    for i in range(steps + 1):
        result[i] = x + dx * i
    return result

def BoundedLogGrid(xMin,xMax,steps):
    result = []
    gridLogSpacing = (np.log(xMax) - np.log(xMin)) / steps
    edx = np.exp(gridLogSpacing)
    result[0]=xMin
    for i in range(1,steps + 1):
        result[i] = result[i-1]*edx
    return result
