class ResultFilterError(Exception):
    """ Use for exceptions in which the filter operationally failed and the
    filter's function cannot be realized. Callers should respond to this as if
    a rejection decision cannot be made. """

    pass

class ResultModifierError(Exception):
    """ Use for exceptions in which the modifier operationally failed and the
    modifier's function cannot be realized. Callers should respond to this as if
    a modification cannot be made to the result. """

    pass