class Engine(object):
    """
    Abstract search engine interface.

    """

    def __init__(self, api_key=None, proxies=None):
        """
        Constructor for SearchEngine.

        :param api_key: string representing unique API access key (optional)
        :param proxies: dict representing proxies to use
                        i.e. {"http":"10.10.1.10:3128", "https":"10.10.1.10:1080"} (optional)
        """
        self.name = self.__class__.__name__
        self.api_key = api_key
        self.proxies = proxies

    # TODO Investigate requests exceptions with bad urls, bad keys etc, extend docstring to implementations.

    def search(self, query):
        """
        Performs a search, retrieves the results and returns them as an ifind response.

        N.B. This should be implemented in the derived classes.

        :param query: ifind.search.query.Query object
        :returns ifind.search.response.Response object
        :raises Requests bad url or something

        """
        pass