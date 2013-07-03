ERROR = {999: "Unknown engine error ({0})",
         400: "Bad request sent to search API ({0})",
         401: "Incorrect API Key({0})",
         403: "Correct API but request refused ({0})"}


class EngineException(object):
    """
    Generic engine exception base.

    """
    def __init__(self, engine, message, code=None):

        self.engine = engine + 'Exception'
        self.message = message
        self.code = code

        if code:
            self.message = ERROR.get(code, 999).format(self.code)

        class NewClass(ValueError):
            pass
        NewClass.__name__ = self.engine
        raise NewClass(self.message)