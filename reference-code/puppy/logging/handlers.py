from logging.handlers import RotatingFileHandler
from datetime import datetime


class PermanentRotatingFileHandler(RotatingFileHandler):
    def __init__(self, filename, mode='a', maxBytes=0, encoding=None, delay=0):
        self._original_file = filename
        self._update_filename()
        RotatingFileHandler.__init__(self, filename, mode, maxBytes, 0, encoding, delay)

    def _update_filename(self):
        now = datetime.now()

        self.baseFilename = '%s.%d.%d.%d.%d.%d.%d.%d' % (self._original_file,
                now.year, now.month, now.day, now.hour, now.minute, now.second,
                now.microsecond)

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None

        self._update_filename()

        self.mode = 'w'
        self.stream = self._open()


class GzipRotatingFileHandler(PermanentRotatingFileHandler):
    def __init__(self, filename, mode='a', maxBytes=0, encoding=None, delay=0):
        super(GzipRotatingFileHandler, self).__init__(filename, mode, maxBytes, encoding, delay)
        self._len = 0

    def emit(self, record):
        super(GzipRotatingFileHandler, self).emit(record)
        msg = "%s\n" % self.format(record)
        self._len += len(msg)

    def doRollover(self):
        super(GzipRotatingFileHandler, self).doRollover()
        self._len = 0

    def shouldRollover(self, record):
        return self._len >= self.maxBytes

    def _update_filename(self):
        super(GzipRotatingFileHandler, self)._update_filename()
        self.baseFilename += '.gz'

    def _open(self):
        import gzip
        return gzip.open(self.baseFilename, self.mode)
