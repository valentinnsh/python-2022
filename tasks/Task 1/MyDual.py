import math
from dataclasses import dataclass
from typing import Union
from numbers import Number


def exp(val: "Dual") -> "Dual":
    return pow(Dual(math.e, 0), val)


def cos(val: "Dual") -> "Dual":
    return Dual(math.cos(val.value), -math.sin(val.value) * val.d)


def sin(val: "Dual") -> "Dual":
    return Dual(math.sin(val.value), math.cos(val.value) * val.d)


def log(val: "Dual") -> "Dual":
    return Dual(math.log(val.value), val.d / val.value)


@dataclass
class Dual:
    value: float
    d: float

    def __add__(self, other: Union["Dual", Number]) -> "Dual":
        if isinstance(other, Dual):
            o_value = other.value
            o_d = other.d
            return Dual(self.value + o_value, self.d + o_d)
        elif isinstance(other, Number):
            return Dual(float(other) + self.value, self.d)

    def subtract(self, other: Union["Dual", Number], is_reflected):
        if isinstance(other, Dual):
            o_value = other.value
            o_d = other.d
            return Dual(self.value - o_value, self.d - o_d)
        elif isinstance(other, Number):
            if is_reflected:
                return Dual(float(other) - self.value, - self.d)
            else:
                return Dual(self.value - float(other), self.d)

    def __sub__(self, other: Union["Dual", Number]) -> "Dual":
        return self.subtract(other, False);

    def __rsub__(self, other: Union["Dual", Number]) -> "Dual":
        return self.subtract(other, True);

    def __mul__(self, other: Union["Dual", Number]) -> "Dual":
        if isinstance(other, Dual):
            o_value = other.value
            o_d = other.d
            return Dual(self.value * o_value, self.value * o_d + self.d * o_value)
        elif isinstance(other, Number):
            return Dual(float(other) * self.value, float(other) * self.d)

    def divide(self, other: Union["Dual", Number], is_reflected):
        if isinstance(other, Dual):
            if other.value == 0:
                raise ZeroDivisionError(
                    "Division of dual numbers is not defined when the real part of the denominator is zero")
            o_value = other.value
            o_d = other.d
            return Dual(self.value / o_value, (self.d * o_value - self.value * o_d) / (o_value ** 2))
        elif isinstance(other, Number):
            if other == 0:
                raise ZeroDivisionError("Dual division by zero")
            if is_reflected:
                return Dual(float(other) / self.value, - float(other)*self.d / self.value**2)
            else:
                return Dual(self.value / float(other), self.d / float(other))

    def __truediv__(self, other: Union["Dual", Number]) -> "Dual":
        return self.divide(other, False)

    def __rtruediv__(self, other: Union["Dual", Number]) -> "Dual":
        return self.divide(other, True)

    def power(self, other: Union["Dual", Number], is_reflected):
        if isinstance(other, Dual):
            o_value = other.value
            o_d = other.d
            return Dual(self.value ** o_value, (o_value * self.value ** (o_value - 1)) * self.d +
                        (self.value ** o_value * math.log(self.value) * o_d))
        elif isinstance(other, Number):
            if is_reflected:
                return Dual(float(other) ** self.value, float(other) ** self.value * math.log(float(other)) * self.d)
            else:
                return Dual(self.value ** float(other), float(other) * (self.value ** (float(other) - 1)) * self.d)

    def __pow__(self, other: Union["Dual", Number]) -> "Dual":
        return self.power(other, False)

    def __rpow__(self, other: Union["Dual", Number]) -> "Dual":
        return self.power(other, True)

    __rmul__ = __mul__
    __radd__ = __add__

    def __neg__(self):
        return Dual(-self.value, -self.d)

    def __pos__(self):
        return self


