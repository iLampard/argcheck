<table>
<tr>
  <td>Latest Release</td>
  <td><img src="https://img.shields.io/pypi/v/argcheck.svg" alt="latest release" /></td>
</tr>

<tr>
  <td>Build</td>
  <td><img src="https://travis-ci.org/iLampard/argcheck.svg?branch=master" alt="build" /></td>
</tr>

<tr>
  <td>Python version</td>
  <td><img src="https://img.shields.io/badge/python-2.7-blue.svg"/>   <img src="https://img.shields.io/badge/python-3.5-blue.svg"/></td>
  </tr>

</table>



# argcheck

A decorator based implementation of argument checks, whose code is largely referenced from [zipline/utils/input_validation](https://github.com/quantopian/zipline/blob/master/zipline/utils/input_validation.py), provides various functionality in argument validation.
* *prepocessor*: decorator that applies pre-processors to the arguments of a function before calling the function
* *expect_kinds*: decorator to check argument dtype kinds
* *expect_types*: decorator to check argument types
* *optional*: helper of *expect_types* to deal with default argument
* *expect_element*: decorator to check if argument takes a value in expected set of elements
* *expect_bounded* and *expect_strictly_bounded*: decorators to check argument lies inclusively or exclusively within the bounds
* *expect_dimensions*: decorator to check if argument takes in a numpy array with a specific dimensionality
* *coerce* and *coerce_types*: decorators that deal with type coercions


### Usage
``` python
from argcheck import *
```

### Install

``` python
pip install argcheck
```

### Quick Start
Two important decorators:
* *prepocessor* accepts a dict that map the argument[key] to processor function[value], whose signature must be (func, argname, argvalue)

    * For example, to process the financial returns data, one usually needs to convert from noncumulative-return to cumulative return, or vice versa. It can be done by prepocessor
``` python

# define a dict struture to store information
return_dict_ = {'type': 'cumul', 'return': pd.Series([1.0, 2.0, 3.0])}

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


calc_mean_return(return_dict=return_dict_)

# 0 Nan
# 1 1.0
# 2 0.5
#   0.75  <- mean value of return
```


* *expect_types*: together with *optional* provides an easy way to do argument type validation


``` python
@expect_types(y=optional(str, int))
def foo(x, y=None):
    return x, y


foo(3) # Ok
foo(3, 'a') # OK
foo(3, [3])
# TypeError: foo() expected a value of type str or int or NoneType for argument 'y',
# but got list instead
```

### Detailed Examples

##### *expect_kinds*: decorator that verifies inputs have expected dtype kinds
``` python
from numpy import int64, int32, float32

@expect_kinds(x='i')
def foo(x):
    return x

foo(int64(2))  # 2
foo(int32(2))  # 2
foo(float32(2))
# Traceback (most recent call last):
#       ...
# TypeError: ...foo() expected a numpy object of kind 'i' for argument 'x',
# but got 'f' instead.

```

##### *expect_types*: decorator that verifies inputs have expected types

``` python
@expect_types(x=int, y=str)
def foo(x, y):
    return x, y


foo(2, '3')  # (2, '3')


foo(2.0, '3')
# Traceback (most recent call last):
# ...
# TypeError: ...foo() expected a value of type int for argument 'x',
# but got float instead.


```

works on class member functions with default argument as well

``` python
class test(object):
    @expect_types(y=(int, str))
    def __init__(self, x, y=3):
        pass


test(x=3)  # OK
test(x=3, y=5) # OK
test(x=1, y=[3])
# Traceback (most recent call last):
# ...
# TypeError: __init__() expected a value of type int or str for argument 'y',
# but got list instead

```


##### *optional*: helper for use with *expect_types* when an input can be `type` or 'tuple of types' or `None`.

``` python
isinstance({}, optional(dict))  # True
isinstance(None, optional(dict))  # True
isinstance(1, optional(dict))  # False
isinstance(1, optional(dict, int))  # True
```
``` python

# used with expect_types
class test2(object):
    @expect_types(y=optional(int, str))
    def __init__(self, x, y=None):
        pass


test2(3)  # OK
test2(3, [2])
# TypeError: __init__() expected a value of type int or str or NoneType for argument 'y',
# but got list instead.

```


##### *expect_element*: decorator that verifies inputs are elements of some expected collection

``` python
@expect_element(x=('a', 'b'))
def foo(x):
    return x.upper()

foo('a')  # 'A'
foo('c')
# ValueError: foo() expected a value in ('a', 'b') for argument 'x',
# but got 'c' instead.
```


##### *expect_bounded*: decorator verifying that inputs fall INCLUSIVELY between bounds
* Bounds should be passed as a pair of ``(min_value, max_value)``.
    ``None`` may be passed as ``min_value`` or ``max_value`` to signify that
    the input is only bounded above or below.

``` python
@expect_bounded(x=(1, 5))
def foo(x):
    return x + 1


foo(3)  # 4
foo(6)
# ValueError: foo() expected a value inclusively between 1 and 5 for argument 'x',
# but got 6 instead


```


``` python
@expect_bounded(x=(1, None))
def foo(x):
    return x + 1


foo(3)  # 4
foo(0)
# ValueError: foo() expected a value greater than or equal to 1 for argument 'x',
# but got 0 instead.


```


##### *expect_strictly_bounded*: decorator verifying that inputs fall EXCLUSIVELY between bounds

``` python

@expect_strictly_bounded(x=(1, 5))
def foo(x):
    return x + 1

foo(5)
# ValueError: foo() expected a value exclusively between 1 and 5 for argument 'x',
# but got 5 instead.
```


##### *expect_dimensions*: decorator that verifies inputs are numpy arrays with a specific dimensionality

``` python

from numpy import array

@expect_dimensions(x=1, y=2)
def foo(x, y):
    return x[0] + y[0, 0]

foo(array([1, 1]), array([[1, 1], [2, 2], [3, 4]])) #ok
foo(array([1, 1]), array([[1, 1], [2, 2]]))  # ok
foo(array([1, 1]), array([1, 1]))

# ValueError: foo() expected a 2-D array for argument 'y',
# but got a 1-D array instead.

```

##### *coerce*: decorator that coerces inputs of a given type by passing them to a callable

``` python
@preprocess(x=coerce(str, int, base=2), y=coerce(str, int, base=2))
def add_binary_strings(x, y):
    return bin(x + y)[2:]

print add_binary_strings('101', '001')  # 110


```


##### *coerce_types*: decorator that applies type coercions
* input param: dict[str -> (type, callable)]
    * Keyword arguments mapping function parameter names to pairs of
         (from_type, to_type)

``` python
@coerce_types(x=(float, int), y=(int, str))
def func(x, y):
    return (x, y)

func(1.0, 3)   # (1, '3')

```

Please see [example](/argcheck/example.py) for details


