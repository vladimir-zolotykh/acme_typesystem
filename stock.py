#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import unittest


class Descriptor:
    def __set_name__(self, owner, name):
        self.name = "_" + name

    def __init__(self, **opts):
        for key, value in opts.items():
            setattr(self, key, value)

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


class Stock:
    name = MaxSizedString(size=8)
    shares = UnsignedInteger()
    price = UnsignedFloat()

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price


class TestStock(unittest.TestCase):
    def setUp(self):
        self.stock = Stock("ACME", 90, 120.3)

    def test_10_name(self):
        self.assertEqual(self.stock.name, "ACME")


if __name__ == "__main__":
    unittest.main()
