#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import unittest


class Descriptor:
    def __init__(self, name=None, **opts):
        if name is not None:
            self.name = "_" + name
        for key, value in opts.items():
            setattr(self, key, value)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        setattr(instance, self.name, value)


class Typed(Descriptor):
    expected_type = type(None)

    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f"{instance} must be of type {self.expected_type}")
        super().__set__(instance, value)


class MaxSized(Descriptor):
    def __init__(self, **opts):
        if "size" not in opts:
            raise TypeError("Missed 'size' option")
        super().__init__(**opts)


class Unsigned(Descriptor):
    def __set__(self, instance, value):
        if value < 0:
            raise ValueError(f"{value}: must not be negative")
        super().__set__(instance, value)


class String(Typed):
    expected_type = str


class MaxSizedString(String, MaxSized):
    def __set__(self, instance, value):
        if len(value) >= self.size:
            raise ValueError(f"Lenght of {value} must not exceed {self.size}")
        super().__set__(instance, value)


class Float(Typed):
    expected_type = float


class UnsignedFloat(Float, Unsigned):
    pass


class Integer(Typed):
    expected_type = int


class UnsignedInteger(Integer, Unsigned):
    pass


class MetaDescriptors(type):
    def __new__(cls, clsname, bases, clsdict):
        for name, value in clsdict.items():
            if isinstance(value, Descriptor):
                setattr(value, "name", "_" + name)
        return super().__new__(cls, clsname, bases, clsdict)


class Stock(metaclass=MetaDescriptors):
    name = MaxSizedString(size=8)
    shares = UnsignedInteger()
    price = UnsignedFloat()

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price


def astuple(stock: Stock) -> tuple[str, int, float]:
    return tuple(stock.__dict__.values())


ACME = ("ACME", 50, 91.1)


class TestStock(unittest.TestCase):
    def setUp(self):
        self.stock = Stock(*ACME)

    def test_20_name(self):
        self.assertEqual(astuple(self.stock), ACME)

    def test_30_allfields(self):
        self.assertEqual(astuple(self.stock), ACME)

    def test_40_shares(self):
        with self.assertRaises(ValueError):
            self.stock.shares = -10

    def test_50_price(self):
        with self.assertRaises(TypeError):
            self.stock.price = "a lot"

    def test_60_name(self):
        with self.assertRaises(ValueError):
            self.stock.name = "ABRACADABRA"


if __name__ == "__main__":
    unittest.main()
