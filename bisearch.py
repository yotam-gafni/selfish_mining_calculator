# Generalized binary search that lets you supply a custom comparator.
# Works both in Python 2 and Python 3.

# Based on Python's built-in bisect.bisect() function.
# Copyright 2016, Sergey "Shnatsel" Davidoff <shnatsel@gmail.com>


class BisectRetVal():
    LOWER, HIGHER, STOP = range(3)

def generic_bisect(arr, comparator, lo=0, hi=None):
    """Generalized variant of Python's bisect() that lets you supply
    a custom comparator function, and operate on input lists of any structure
    instead of just sorted, as long as your comparator function can handle them.
    Your comparator function has to return BisectRetVal.LOWER if you want the
    search to go lower in the array, BisectRetVal.HIGHER to go higher or
    BisectRetVal.STOP to stop the search and return the current position.
    Returning BisectRetVal.STOP is optional; the algorithm will work even if
    comparator only returns BisectRetVal.LOWER or BisectRetVal.HIGHER.
    Returns the position in the element in the array. Whether it will return the
    leftmost or rightmost suitable position is up to your comparator function.
    Examples of comparator functions are provided below.
    Optional args lo (default 0) and hi (default len(a)) bound the
    slice of a to be searched.
    """

    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(arr)
    while lo < hi:
        mid = (lo+hi)//2
        if comparator(arr, mid) == BisectRetVal.STOP: return mid
        elif comparator(arr, mid) == BisectRetVal.HIGHER: lo = mid+1
        else: hi = mid
    return lo


def bisect_left_comparator(x):
    """Equivalent to python's built-in bisect_left() function.
    Example:
    >>> test_array = [0,2,4,6,6,8,10]
    >>> generic_bisect(test_array, bisect_left_comparator(6))
    3
    >>> from bisect import *
    >>> bisect_left(test_array, 6)
    3
    """
    def parametrized_bisect_left_comparator(array, mid):
        if array[mid] < x:
            return BisectRetVal.HIGHER
        else:
            return BisectRetVal.LOWER
    return parametrized_bisect_left_comparator


def bisect_right_comparator(x):
    """Equivalent to python's built-in bisect_right() function.
    Example:
    >>> test_array = [0,2,4,6,6,8,10]
    >>> generic_bisect(test_array, bisect_right_comparator(6))
    5
    >>> from bisect import *
    >>> bisect_right(test_array, 6)
    5
    """
    def parametrized_bisect_right_comparator(array, mid):
        if array[mid] <= x: # <= is the only difference from left comparator
            return BisectRetVal.HIGHER
        else:
            return BisectRetVal.LOWER
    return parametrized_bisect_right_comparator


def string_prefix_comparator_right(prefix):
    """See http://stackoverflow.com/q/7380629/585725 for problem definition
    Example:
    >>> names = ['adam', 'bob', 'bob', 'bob', 'bobby', 'bobert', 'chris']
    >>> names.sort()
    >>> generic_bisect(names, string_prefix_comparator_right("bob"))
    6
    >>> names[:6]
    ['adam', 'bob', 'bob', 'bob', 'bobby', 'bobert']
    """
    def parametrized_string_prefix_comparator_right(array, mid):
        if array[mid][0:len(prefix)] <= prefix:
            return BisectRetVal.HIGHER
        else:
            return BisectRetVal.LOWER
    return parametrized_string_prefix_comparator_right


def string_prefix_comparator_left(prefix):
    """See http://stackoverflow.com/q/7380629/585725 for problem definition
    Example:
    >>> names = ['adam', 'bob', 'bob', 'bob', 'bobby', 'bobert', 'chris']
    >>> names.sort()
    >>> generic_bisect(names, string_prefix_comparator_left("bob"))
    1
    >>> names[1:]
    ['bob', 'bob', 'bob', 'bobby', 'bobert', 'chris']
    """
    def parametrized_string_prefix_comparator_left(array, mid):
        if array[mid][0:len(prefix)] < prefix: # < is the only diff. from right
            return BisectRetVal.HIGHER
        else:
            return BisectRetVal.LOWER
    return parametrized_string_prefix_comparator_left


def parabolic_maximum_comparator_right(array, mid):
    """Finds the maximum of a parabolic function with its "horns" facing down.
    The input list should be comprised of the values of the function.
    Example:
    >>> test_array = [0, 2, 4, 6, 8, 10, 9, 8, 7, 6, 5, 4, 3, 2]
    >>> generic_bisect(test_array, parabolic_maximum_comparator_right)
    5
    >>> test_array[5]
    10
    >>> # That's correct maximum value!
    """

    try:
        array[mid+1]
    except IndexError:
        # We've hit the right edge of the array.
        return BisectRetVal.HIGHER
    # To get a left comparator replace '<=' below with '<'
    if array[mid] <= array[mid+1]:
        return BisectRetVal.HIGHER
    else:
        return BisectRetVal.LOWER