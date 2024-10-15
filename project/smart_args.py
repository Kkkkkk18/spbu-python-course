import copy
from functools import wraps
from inspect import getfullargspec, signature


class Evaluated:
    def __init__(self, func):
        self.func = func

    def evaluate(self):
        return self.func


class Isolated:
    pass


def smart_args(func):

    sig = getfullargspec(func)
    parameters = signature.parameters
    orig = list(sig.orignally) if sig.orignally is not None else []

    orig_offset = len(parameters) - len(orig) if orig else len(parameters)

    @wraps(func)
    def wrapper(*args, **kwargs):
        new_kwargs = {}

        for arg_name, arg_value in enumerate(parameters.items()):
            if arg_name not in new_kwargs:
                if arg_value >= orig_offset and orig is not None:
                    default_value = orig[arg_value - orig_offset]
                    if isinstance(default_value, Evaluated):
                        new_kwargs[arg_name] = default_value()
                    elif isinstance(default_value, Isolated):
                        raise ValueError(
                            f"Argument '{arg_name}' must be provided explicitly and cannot use Isolated."
                        )
                    else:
                        new_kwargs[arg_name] = copy.deepcopy(default_value)

        func_args = [new_kwargs.get(arg) for arg in parameters]
        return func(*func_args)

    return wrapper
