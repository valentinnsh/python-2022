import random
import unittest
import MyDual
import math
import sympy
import RandomFunctionsGenerator
from typing import Union
from MyDual import Dual
from numbers import Number
from sympy.calculus.util import continuous_domain
from numpy.testing._private.parameterized import parameterized


def exp(val:  Union["Dual", Number, sympy.Function]):
    if isinstance(val, Dual):
        return MyDual.exp(val);
    elif isinstance(val, Number):
        return math.exp(val)
    elif isinstance(val, sympy.Symbol):
        return sympy.exp(val)


def cos(val:  Union["Dual", Number, sympy.Function]):
    if isinstance(val, Dual):
        return MyDual.cos(val);
    elif isinstance(val, Number):
        return math.cos(val)
    elif isinstance(val, sympy.Symbol):
        return sympy.cos(val)


def sin(val:  Union["Dual", Number, sympy.Function]):
    if isinstance(val, Dual):
        return MyDual.sin(val);
    elif isinstance(val, Number):
        return math.sin(val)
    elif isinstance(val, sympy.Symbol):
        return sympy.sin(val)


def log(val:  Union["Dual", Number, sympy.Function]):
    if isinstance(val, Dual):
        return MyDual.log(val);
    elif isinstance(val, Number):
        return math.log(val)
    elif isinstance(val, sympy.Symbol):
        return sympy.log(val)


def pick_valid_test_value(func, x):
    # pick value from continuous_domain
    domain = continuous_domain(func, x, sympy.S.Reals)

    if type(domain) == sympy.sets.sets.EmptySet:
        print("Function is not defined on R")
        return None

    subdomain = domain

    if type(domain) == sympy.sets.fancysets.Reals:
        subdomain = sympy.Interval(-1000, 1000)

    while not subdomain.is_Interval:
        subdomain = subdomain.args[0]

    start = subdomain.inf if not (math.isinf(subdomain.inf) and subdomain.inf < 0) else subdomain.sup - 1000
    end = subdomain.sup if not (math.isinf(subdomain.sup) and subdomain.sup > 0) else subdomain.inf + 1000

    return random.uniform(start, end)


def pre_generated_functions_test_case_source():
    with open('functions.dat') as file:
        return [line.rstrip() for line in file]


class RandomGeneratorTestCase(unittest.TestCase):
    @unittest.skip("Probably deprecated, left for history sake")
    def test_with_random_generator(self):
        function_str = RandomFunctionsGenerator.generate(random.randint(4, 20))
        func = eval('lambda x: ' + function_str)
        print(f'Function: {function_str}')

        x = sympy.symbols('x', real=True)
        parsed = sympy.parse_expr(function_str[9:], locals())
        print(f'Parsed by simpy: {parsed}')
        df = sympy.diff(parsed, x)
        print(f'Derivative by simpy: {df}')

        val = pick_valid_test_value(parsed, x)
        print(f'Value: {val}')
        if val is None:
            self.skipTest('Function is not defined on R')

        self.assertAlmostEqual(func(Dual(val, 1)).d, df.evalf(subs={x: val}))

    @parameterized.expand(pre_generated_functions_test_case_source())
    def test_with_pre_generated_functions(self, func_str):
        func = eval('lambda x: ' + func_str)
        x = sympy.symbols('x', real=True)
        parsed = sympy.parse_expr(func_str, locals())
        df = sympy.diff(parsed, x)

        val = pick_valid_test_value(parsed, x)

        dual_result = func(Dual(val, 1))
        # Assert if delta is less than 1% of the result. More precise may fail on very big or very small numbers
        # It's probably better to just filter out functions like that on generation stage, but I didn't manage to do it in a reasonable time
        self.assertAlmostEqual(dual_result.d, df.evalf(subs={x: val}), delta=abs(dual_result.d * 0.01))

