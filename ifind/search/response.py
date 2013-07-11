class Response(object):
    """
    Models a Response object for use with ifind's search interface.

    Response Attributes:
        query_terms:  string representation of original query terms
        results:      list representation of retrieved results (each result being a dict)
                      i.e {'title': Crow Rearing, 'url': http://etc.com, 'summary': How to rear crows?}
        result_total: integer representation of total results retrieved
    """

    def __init__(self, query_terms):
        """
        Response constructor.

        Args:
            query_terms (str): original query terms

        Attributes:
            results (list): list of retrieved results (each result being a Result object)
            result_total (int): total results retrieved

        Usage:
            response = Response(query.terms)

        """
        self.query_terms = query_terms
        self.results = []
        self.result_total = 0

    def add_result(self, title="", url="", summary="", **kwargs):
        """
        Adds a result to Response's results list.

        Kwargs:
            title (str): title of search result
            url (str): url of search result
            summary (str): summary of search result
            **kwargs: further optional result attributes

        Usage:
            response.add_result(title="don's shop", url="www.dons.com", summary="a very nice place")

        """
        self.results.append(Result(title, url, summary, **kwargs))
        self.result_total += 1

    def __str__(self):
        """
        Returns human-readable string representation of response object.

        Returns:
            str: formatted new-lined list of results with info above

        Usage:
            print response

        """
        half_string = 'Result_total: {0}\nQuery_terms: {1}\nResults:\n\n'.format(self.result_total, self.query_terms)
        end_string = '\n\n'.join(['{0}'.format(result) for result in self.results])

        return half_string + end_string

    def __iter__(self):
        """
        Implements iterator for Response, returning a single result at a time.
        Uses generator function to lazy load results.

        Usage:
            for result in response:
                print result

        """
        for result in self.results:
            yield result

    def __len__(self):
        """
        Implements len() builtin for Response.

        Returns:
            int: number of results within response

        Usage:
            print len(response) --> 15

        """
        return self.result_total

    def __iadd__(self, other):
        """
        Overrides '+=' operator, adds other.results to self.results.

        Usage:
            print len(response1) --> 10
            print len(response2) --> 15
            response1 += response2
            print len(response1) --> 25

        """
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
    """
    Models a Result object for use with ifind's Response class.

    """
    def __init__(self, title="", url="", summary="", **kwargs):
        """
        Result constructor.

        Kwargs:
            title (str): title of search result
            url (str): url of search result
            summary (str): summary of search result
            **kwargs: further optional result attributes

        Usage:
            result = Result(title="pam's shop", url="www.pam.com", summary="a nice place")

        """
        self.title = title
        self.url = url
        self.summary = summary

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.__dict__ = {key: value.encode('utf-8').rstrip() for key, value in self.__dict__.items()}

    def __str__(self):
        """
        Returns human-readable string representation of result object.

        Returns:
            str: formatted new-lined list of result attributes

        Usage:
            print result

        """
        return "\n".join("{0}: {1}".format(key, value) for key, value in self.__dict__.items())