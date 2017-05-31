# -*- coding: utf-8 -*-

from argcheck.preprocess import preprocess
from argcheck.validation import (expect_types,
                                 expect_bounded,
                                 expect_dimensions,
                                 expect_dtypes,
                                 ensure_dtype,
                                 expect_element,
                                 expect_kinds,
                                 expect_strictly_bounded,
                                 optional,
                                 optionally,
                                 coerce_types,
                                 coerce,
                                 coerce_string)

import pandas as pd


# define the processor function
def ensure_noncumul_return(func, argname, arg):
    ret = {}
    if not isinstance(arg, dict):
        return
    if arg['type'] == 'cumul':
        ret['return'] = arg['return'].pct_change()
        ret['type'] = 'noncumul'
        return ret
    else:
        return arg

# apply preprocess decorator to ensure the argument has noncumul return
@preprocess(return_dict=ensure_noncumul_return)
def calc_mean_return(return_dict):
    return return_dict['return'], return_dict['return'].mean()

# define a dict struture to store information
return_dict_ = {'type': 'cumul', 'return': pd.Series([1.0, 2.0, 3.0])}

print calc_mean_return(return_dict=return_dict_)


@expect_types(y=optional(str, int))
def foo(x, y=None):
    return x, y


foo(3) # Ok
foo(3, 'a') # OK
foo(3, [3]) # TypeError


def preprocessor(func, argname, arg):
    if not isinstance(arg, int):
        raise TypeError('arg must be int')
    return arg


@preprocess(a=optionally(preprocessor))
def f(a):
    return a


f(1)  # call with int
# f('a')  # call with not int
#    Traceback (most recent call last):
#       ...
#    TypeError: arg must be int
f(None) is None  # call with explicit None
#    True








from numpy import int64, int32, float32


@expect_kinds(x='i')
def foo(x):
    return x


foo(int64(2))  # 2
foo(int32(2))  # 2


# foo(float32(2))


# Traceback (most recent call last):
#       ...
# TypeError: ...foo() expected a numpy object of kind 'i' for argument 'x',
# but got 'f' instead.


@expect_types(x=int, y=str)
def foo(x, y):
    return x, y


foo(2, '3')  # (2, '3')


# foo(2.0, '3')
# Traceback (most recent call last):
# ...
# TypeError: ...foo() expected a value of type int for argument 'x',
# but got float instead.

class test(object):
    @expect_types(y=(int, str))
    def __init__(self, x, y=3):
        pass


test(x=3)
test(x=3, y=5)
# test(x=1, y=[3])
# TypeError: __init__() expected a value of type int or str for argument 'y', but got list instead


print isinstance({}, optional(dict))  # True
print isinstance(None, optional(dict))  # True
print isinstance(1, optional(dict, int))  # False


class test2(object):
    @expect_types(y=optional(int, str))
    def __init__(self, x, y=None):
        pass


test2(3)


# test2(3, [2])

@expect_element(x=('a', 'b'))
def foo(x='a'):
    return x.upper()


foo('a')


# foo('c')


@expect_bounded(x=(1, 5))
def foo(x):
    return x + 1


foo(3)  # 4


# foo(6)
# ValueError: foo() expected a value inclusively between 1 and 5 for argument 'x',
# but got 6 instead


@expect_bounded(x=(1, None))
def foo(x):
    return x + 1


foo(3)  # 4


# foo(0)
# ValueError: foo() expected a value greater than or equal to 1 for argument 'x',
# but got 0 instead.


@expect_strictly_bounded(x=(1, 5))
def foo(x):
    return x + 1


# foo(5)



from numpy import array


@expect_dimensions(x=1, y=2)
def foo(x, y):
    return x[0] + y[0, 0]


foo(array([1, 1]), array([[1, 1], [2, 2], [3, 4]]))


# foo(array([1, 1]), array([1, 1]))

# ValueError: foo() expected a 2-D array for argument 'y',
# but got a 1-D array instead.


@preprocess(x=coerce(float, int), y=coerce(float, int))
def floordiff(x, y):
    return x - y


print floordiff(3.2, 2.5)


@preprocess(x=coerce(str, int, base=2), y=coerce(str, int, base=2))
def add_binary_strings(x, y):
    return bin(x + y)[2:]


print add_binary_strings('101', '001')

print coerce_string(('a', 'b'))
