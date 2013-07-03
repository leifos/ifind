class Response(object):
    """
    Models a Response object for use with ifind's search interface.

    Response Attributes:
        query_terms:  string representation of original query terms
        results:      list representation of retrieved results (each result being a dict)
                      i.e {'title': Crow Rearing, 'url': http://etc.com, 'summary': How to rear crows?}
        result_total: integer representation of total results retrieved
    """

    def __init__(self, results=None):
        """
        Constructs Response object.

        """
        self.query_terms = ''
        self.results = results or []
        self.result_total = 0

    def __iter__(self):
        for result in self.results:
            yield result

    def add_result(self, title, url, summary=''):
        """
        :param title: string representation of result title
        :param url:  string representation of result url
        :param summary: string representation of result's summary

        """
        self.results.append(Result(title, url, summary))
        self.result_total += 1

    def print_results(self):
        for result in self.results:
            print result

    def __str__(self):
        """
        Returns human-readable string representation of query object.

        """
        return '\n'.join(['{0}: {1}'.format(key, value)
                          for (key, value) in self.__dict__.items()])

    def __iadd__(self, other):
        self.results += other.results
        self.result_total += other.result_total
        return self

    def from_oss_feed(self, oss_xml_feed):
        """
        Populates the Response object using the data from an Open Search response feed

        """
        pass

    def to_rss(self):
        """
        Creates an RSS feed from a Response object.

        Returns:

        * response_xml (str): Response as RSS feed
        """
        pass

    def to_atom(self):
        """
        Creates an XML from a OpenSearch Response.

        Returns:

        * response_xml (str): OpenSearch Response as an ATOM feed
        """
        pass

    def to_json(self):
        """
        Creates JSON from a Response object.

        Returns:

        * response_json (str): Response as JSON
        """
        pass


class Result(object):

    def __init__(self, title, url, summary=''):
        self.title = title
        self.summary = summary
        self.url = url

    def __str__(self):
        return 'Title: {0}\nSummary: {1}\nURL: {2}'.format(self.title, self.summary, self.url)
