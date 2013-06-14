class QueryFilterError(Exception):
    """ Use for exceptions in which the filter operationally failed and the
    filter's function cannot be realized. Callers should respond to this as if
    a modification or rejection decision cannot be made, as opposed to
    :class:`puppy.query.QueryRejectionError`, in which case the query should
    not be issued. """

    pass

class QueryModifierError(Exception):
    """ Use for exceptions in which the modifier operationally failed and the
    modifier's function cannot be realized. Callers should respond to this as if
    a modification or rejection decision cannot be made, as opposed to
    :class:`puppy.query.QueryRejectionError`, in which case the query should
    not be issued. """

    pass


class QueryRejectionError(Exception):
    """ Raise when a filter rejects a query, e.g., because profanity is
    detected. """

    pass
