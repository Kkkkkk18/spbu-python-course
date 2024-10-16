def uncurry_explicit(function, arity):

    """
    Uncurries a curried function to accept multiple arguments at once.

    Parameters:
    function (callable): The curried function to be uncurried.
    arity (int): The number of arguments the function expects.

    Returns:
    function: A function that accepts all arguments at once.
    Raises:
    ValueError: If the arity is negative.
    TypeError: If the number of arguments provided to the uncurried function does not match the arity.

    """

    if arity < 0:
        raise ValueError("Arity cannot be negative")

    def uncurried(*args):

        if len(args) != arity:
            raise TypeError(f"Expected {arity} arguments, received {len(args)}")

        if arity == 0:
            return function()

        current_func = function

        for arg in args:

            current_func = current_func(arg)
        return current_func

    return uncurried
