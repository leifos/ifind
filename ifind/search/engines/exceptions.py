ERROR = {'default': "Unknown engine error ({0})",
         400: "Bad request sent to search API ({0})",
         401: "Incorrect API Key ({0})",
         403: "Correct API but request refused ({0})",
         404: "Bad request sent to search API ({0})"}


class SearchException(Exception):
    """
    Generic engine exception base.

    """
    def __init__(self, engine, message):

        self.engine = engine + 'Exception'
        Exception.__init__(self, message)

        class NewClass(ValueError):
            pass

        NewClass.__name__ = self.engine
        raise NewClass(self.message)


class EngineException(SearchException):

    def __init__(self, engine, message, code=None):

        self.code = code
        if code:
            self.message = ERROR.get(code, ERROR['default']).format(self.code)
        SearchException.__init__(self, engine, message)