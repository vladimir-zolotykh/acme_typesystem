#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from functools import cache
import time


def factorial(n):
    if n in (1, 2):
        return n
    else:
        return n * factorial(n - 1)


class lazyproperty:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        val = self.func()
        setattr(instance, self.func.__name__, val)
        return val


class TestClass:
    @lazyproperty
    @cache
    def long_function(val=12):
        print("Running long_function ...")
        time.sleep(3)
        return val * 10


if __name__ == "__main__":
    test = TestClass()
    print(test.long_function)
    print(test.long_function)
