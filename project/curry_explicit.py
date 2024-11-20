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

    def curried(*args):
        if len(args) == arity:
            return function(*args)
        elif len(args) > arity:
            raise TypeError(f"Expected {arity} arguments, received {len(args)}")
        return lambda *new_args: curried(*(args + new_args))

    return curried
