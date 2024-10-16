import copy
from functools import wraps
from inspect import signature


class Evaluated:

    """
    A class used to wrap functions that need to be evaluated when the decorated function is called.
    """

    def __init__(self, func):

        """
        Initializes the Evaluated instance with a function.

        Parameters:
        func (callable): The function to be evaluated.
        """

        self.func = func

    def evaluate(self):

        """
        Returns the wrapped function.

        Returns:
        callable: The wrapped function.
        """

        return self.func


class Isolated:

    """Fictitious class-flag."""

    pass


def smart_args(func):

    """
    A decorator that enhances the handling of function arguments by evaluating and isolating
    specific types of arguments.

    Parameters:
    func (callable): The function to be decorated.

    Returns:
    callable: A wrapper function that handles the evaluation and isolation of arguments.

    Raises:
    ValueError: If an argument marked as Isolated is used as a default value for an Evaluated argument.
    ValueError: If a required Isolated argument is not provided correctly.
    """

    sig = signature(func)
    param = sig.parameters

    @wraps(func)
    def wrapper(*args, **kwargs):

        """
        An internal wrapper function generated by the smart_args decorator. It handles the
        evaluation and isolation of arguments before calling the original function.

        Parameters:
        args: Positional arguments passed to the decorated function.
        kwargs: Keyword arguments passed to the decorated function.

        Returns:
        The result of calling the original function with the processed arguments.

        Raises:
        AssertionError: If any argument is an instance of Evaluated or Isolated.
        ValueError: If an argument marked as Isolated is used as a default value for an Evaluated argument.
        ValueError: If a required Isolated argument is not provided correctly.
        """

        new_kwargs = {}

        assert all(not isinstance(arg, (Evaluated, Isolated)) for arg in args)
        assert all(not isinstance(kwargs[key], (Evaluated, Isolated)) for key in kwargs)

        for arg_name, arg_value in param.items():
            if arg_name in kwargs and not isinstance(
                arg_value.default, (Isolated, Evaluated)
            ):
                new_kwargs[arg_name] = kwargs[arg_name]
            elif isinstance(arg_value.default, Evaluated):
                d_value = arg_value.default.func
                if d_value == Isolated:
                    raise ValueError("Isolated is an argument for Evaluated.")
                if arg_name in kwargs:
                    new_kwargs[arg_name] = kwargs[arg_name]
                else:
                    new_kwargs[arg_name] = d_value()
            elif isinstance(arg_value.default, Isolated):
                if arg_name in kwargs:
                    new_kwargs[arg_name] = copy.deepcopy(kwargs[arg_name])
                else:
                    raise ValueError(
                        f"Argument '{arg_name}' must be provided correctly"
                    )
        return func(*args, **new_kwargs)

    return wrapper
