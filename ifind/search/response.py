class Response(object):
    """
    Data model for search results.  Response has four main attributes:
    * results_per_page: integer
    * total_no_of_results: integer
    * result_page: integer
    * results_list: list of results [{title, link, summary, etc}, ...]
    * search_query: string

    """

    def __init__(self, results=None):

        """Constructor for Response."""
        self.query_terms = ''
        self.result_list = results or []
        self.results_per_page = 0
        self.total_no_of_results = 0
        self.results_page = 1

    def __str__(self):
        return self.query_terms


    def add_result(self, title, link, summary='', **kwargs):
        result_item_dict = {'title': title, 'link': link, 'summary': summary}
        self.result_list.append(result_item_dict)
        self.results_per_page += 1
        self.total_no_of_results += 1

    def print_results(self):
        for r in self.result_list:
            print r


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

