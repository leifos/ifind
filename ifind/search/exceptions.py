class SearchException(Exception):
    """
    Generic search exception base.

    """
    pass


class MissingKeyError(SearchException):
    """
    Represents a missing API key exception.

    """
    pass


