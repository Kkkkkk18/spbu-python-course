def uncurry_explicit(function, arity):

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
