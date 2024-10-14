def curry_explicit(function, arity):

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
