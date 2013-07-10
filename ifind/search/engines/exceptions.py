# TODO When raising an exception pass a lambda function, the function being the module/path/name thing

ERROR = {'default': "Unknown engine error ({0})",
         400: "Bad request sent to search API ({0})",
         401: "Incorrect API Key ({0})",
         403: "Correct API but request refused ({0})",
         404: "Bad request sent to search API ({0})"}


class SearchException(Exception):
    """
    Class representing an ifind search exception.
    Automatically names itself to module exception was raised from.

    """
    def __init__(self, module, message):
        """
        SearchException constructor.

        Args:
            module (str): name of module that's raising exception
            message (str): exception message to be displayed

        Usage:
            raise SearchException("Test", "this is an error")

        """

        self.engine = module + 'Exception'
        Exception.__init__(self, message)

        class NewClass(ValueError):
            pass

        NewClass.__name__ = self.engine
        raise NewClass(self.message)


class EngineException(SearchException):
    """
    Class representing an ifind engine exception.
    Returns specific code message if status specified.

    """

    def __init__(self, engine, message, code=None):
        """
        EngineException constructor.

        Args:
            engine (str): name of engine that's raising exception
            message (str): exception message to be displayed (ignored usually here)

        Kwargs:
            code (int): reponse status code of issued request

        Usage:
            raise EngineException("Bing", "", code=200)

        """
        self.code = code
        if code:
            self.message = ERROR.get(code, ERROR['default']).format(self.code)
        SearchException.__init__(self, engine, message)