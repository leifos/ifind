from ifind.search.cache import RedisConn


class Throttle(object):
    """
    An object representing a throttle, assigned to an Engine instance upon its
    instantiation. Throttle prevents the engine from further search requests until
    rate limit has expired.

    """

    def __init__(self, instance, seconds_per_request):
        """
        Throttle constructor.

        Args:
            instance (ifind Engine): reference to engine that's instantiating the throttle
            seconds_per_request (int): search rate limit in seconds

        Usage:
            See EngineFactory.

        """

        # throttle key determined by engine name and instance id
        self.key = "throttleID::{0}{1}".format(instance.name.lower(), id(instance))
        # redis connection
        self.cache = RedisConn().connect()
        # current rate limit
        self.rate_limit = seconds_per_request

    def is_active(self):
        """ Returns True if current engine instance is being throttled. """
        return True if self.cache.get(self.key) else False

    def set_limit(self, seconds_per_request):
        """ Stops active throttling on current engine instance and sets the rate limit. """
        self.stop()
        self.rate_limit = seconds_per_request

    def start(self):
        """ Unless rate limit is 0, it starts throttling current engine instance. """
        if self.rate_limit:
            self.cache.set(self.key, 'foo', ex=self.rate_limit)

    def stop(self):
        """ Stops active throttling on current engine instance. """
        self.cache.delete(self.key)