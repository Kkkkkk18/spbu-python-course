def curry_explicit(function, arity):

    """
    Curry a function explicitly with a specified arity.

    This function takes a function and an arity (the number of arguments the function expects)
    and returns a curried version of the function. The curried function will accept arguments
    one at a time until the specified arity is reached, at which point the original function
    will be called with all the accumulated arguments.

    Parameters:
    function (callable): The function to be curried.
    arity (int): The number of arguments the function expects.

    Returns:
    function: A curried version of the input function.

    Raises:
    ValueError: If the arity is negative.
    TypeError: If the number of arguments provided to the curried function exceeds the arity.

    Example usage:
    ```python
    def add(x, y, z):
        return x + y + z

    curried_add = curry_explicit(add, 3)
    result = curried_add(1)(2)(3)
    print(result)  # Output: 6
    ```
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
