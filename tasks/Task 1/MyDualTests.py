import unittest
import MyDual
import math
from typing import Union
from MyDual import Dual
from numbers import Number
from scipy.misc import derivative
from numpy.testing._private.parameterized import parameterized


def exp(val:  Union["Dual", Number]):
    if isinstance(val, Dual):
        return MyDual.exp(val);
    elif isinstance(val, Number):
        return math.exp(val)


def cos(val:  Union["Dual", Number]):
    if isinstance(val, Dual):
        return MyDual.cos(val);
    elif isinstance(val, Number):
        return math.cos(val)


def sin(val:  Union["Dual", Number]):
    if isinstance(val, Dual):
        return MyDual.sin(val);
    elif isinstance(val, Number):
        return math.sin(val)


def log(val:  Union["Dual", Number]):
    if isinstance(val, Dual):
        return MyDual.log(val);
    elif isinstance(val, Number):
        return math.log(val)


def derivative_test_case_source():
    return [
            (lambda x: -x, lambda x: -1, 2.0),  # unary minus
            (lambda x: 10 + x + 12.3, lambda x: 1, 2.0),  # addition
            (lambda x: x * x * 12.3, lambda x: 24.6 * x, 2.0),  # multiplication
            (lambda x: 10 / x / x / 12.3, lambda x: - 20 / x / x / x / 12.3, 2.0),  # division
            (lambda x: 10 ** x, lambda x: 10 ** x * log(10), 2.0),  # power
            (lambda x: x ** 10, lambda x: 10 * x ** 9, 2.0),  # power
            (lambda x: x ** x, lambda x: x ** x * (1 + log(x)), 2.0),  # power
            (lambda x: 5 * x ** 2 + 2 * x + 2, lambda x: 10 * x + 2, 2.0)  # example from the task
    ]


def additional_functions_test_case_source():
    return [
            (lambda x: exp(x), lambda x: exp(x), 2.0),
            (lambda x: cos(x), lambda x: -sin(x), 2.0),
            (lambda x: sin(x), lambda x: cos(x), 2.0),
            (lambda x: log(x), lambda x: 1 / x, 2.0),
    ]


def numerical_differentiation_test_case_source():
    return[
        (lambda x: 5 * x * x + 2 * x + 2, 2.0),  # from example
        (lambda x: sin(3 * x) + 2 * x ** 3 - (x * 2 + 1) ** 0.5 + log(x + 1), 2.0),  # from example
        (lambda x: exp(3*x**(-2)) - sin(2*x), 2.0),  # random function I came up with
        (lambda x: cos(log(3*x+1)**2 + 10) - sin(2*x), 2.0),  # random function I came up with
    ]


class FirstTestCase(unittest.TestCase):
    @parameterized.expand(derivative_test_case_source())
    def test_if_derivative_checks_out(self, f, df, x):
        f_dual = f(Dual(x, 1.0))
        self.assertAlmostEquals(f_dual.value, f(x))
        self.assertAlmostEquals(f_dual.d, df(x))


class SecondTestCase(unittest.TestCase):
    @parameterized.expand(additional_functions_test_case_source())
    def test_functions_for_Dual(self, f, df, x):
        f_dual = f(Dual(x, 1.0))
        self.assertAlmostEquals(f_dual.value, f(x))
        self.assertAlmostEquals(f_dual.d, df(x))


class NumericalDifferentiationTestCase(unittest.TestCase):
    @parameterized.expand(numerical_differentiation_test_case_source())
    def test_numerical_differentiation(self, f, x):
        f_dual = f(Dual(x, 1.0))
        self.assertAlmostEquals(f_dual.d, derivative(f, x, dx=1e-6))


if __name__ == '__main__':
    unittest.main()
