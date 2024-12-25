from collections import OrderedDict
from functools import wraps


def cache_results(max_results=0):

    """
    A decorator to cache the results of a function.

    Parameters:
    max_results (int): The maximum number of results to store in the cache.
                      If max_results is 0, the cache will be unlimited.

    Returns:
    function: A decorator that can be applied to a function to cache its results.

    """

    def decorator(func):

        cache = OrderedDict()

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = (tuple(args), frozenset(kwargs.items()))
            if key in cache:
                return cache[key]
            result = func(*args, **kwargs)
            if max_results > 0:
                if len(cache) >= max_results:
                    cache.popitem(last=False)
                cache[key] = result
            return result

        return wrapper

    return decorator
