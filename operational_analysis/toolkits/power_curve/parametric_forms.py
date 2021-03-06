import numpy as np


"""
Power Curves

These curve functions are written in the style of Scipy.optimize:

fun : callable
The objective function to be minimized.
fun(x, *args) -> float
where x is an 1-D array with shape (n,) and args is a tuple of the fixed parameters needed to completely specify the function.

ref: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html#scipy.optimize.minimize

"""


def logistic5param(x, a, b, c, d, g):
    """ Create and return a 5 parameter logistic function

    Args:
        x(numpy.array): input data
        a(float): the minimum value asymptote
        b(float): steepness of the curve
        c(float): the point of inflection
        d(float): the maximum value asymptote
        g(float): asymmetry of the curve

    Returns:
        Function[numpy.ndarray[real]] -> numpy.ndarray[real]
        Function[pandas.Series[real]] -> pandas.Series[real]

    """
    return d+(a-d)/(1+(x/c)**b)**g


def logistic5param_capped(x, a, b, c, d, g, lower, upper):
    """ Create and return a capped 5 parameter logistic function whose output is capped by lower and upper bounds.

    Args:
        x(numpy.array): input data
        a(float): the minimum value asymptote
        b(float): steepness of the curve
        c(float): the point of inflection
        d(float): the maximum value asymptote
        g(float): asymmetry of the curve
        lower(Number): Input values below this number are set to this number.
        upper(Number): Input values above this number are set to this number.

    Returns:
        Function[numpy.ndarray[real]] -> numpy.ndarray[real]
        Function[pandas.Series[real]] -> pandas.Series[real]

    """
    return _cap(logistic5param(x, a, b, c, d, g), lower, upper)


"""
Helpers for Power Curve
"""


def _cap(y, lower, upper):
    if type(y) is np.ndarray:
        y[y < lower] = lower
        y[y > upper] = upper
    else:
        y.loc[y < lower] = lower
        y.loc[y > upper] = upper
    return y
