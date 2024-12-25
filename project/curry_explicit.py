from functools import wraps


def curry_explicit(function, arity):

    """
    Curry a function explicitly with a specified arity.

    Parameters:
    function (callable): The function to be curried.
    arity (int): The number of arguments the function expects.

    Returns:
    function: A curried version of the input function.

    Raises:
    ValueError: If the arity is negative.
    TypeError: If the number of arguments provided to the curried function exceeds the arity.

    """

    if arity < 0:
        raise ValueError("Arity cannot be negative")

    if arity == 0:
        return function

    numargs = 0

    @wraps(function)
    def curried(*args):
        nonlocal numargs
        if numargs != len(args) - 1:
            raise TypeError(f"Expected 1 argument")
        numargs += 1

        if len(args) == arity:
            return function(*args)
        if len(args) < arity:
            return lambda arg: curried(*(args + (arg,)))
        raise TypeError(f"Expected exactly {arity} arguments, but got {len(args)}")

    return curried
