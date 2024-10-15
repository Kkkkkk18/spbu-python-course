from collections import OrderedDict
from functools import wraps


def cache_results(max_results=0):
    def decorator(func):

        cache = OrderedDict()

        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
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


@cache_results(max_results=2)
def add(x, y):
    return x + y
