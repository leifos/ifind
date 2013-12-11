import string

class Query(object):
    """
    Models a Query object for use with ifind's search interface.

    """
    def __init__(self, terms, top=10, lang="", result_type=""):
        """
        Query constructor.

        Args:
            terms (str): query terms to search for.

        Kwargs:
            top (int): maximum number of results to return
            lang (str): preferred language of returned results (engine specific)
            result_type (str): type of query (engine specific)

        Attributes:
            skip (int): offset of starting point for results returned

        Usage:
            query = Query("hello world")
            query = Query("hello world", top=20)

        """
        self.terms = Query.check_input(terms)
        self.parsed_terms = None
        self.result_type = result_type.lower()
        self.lang = lang
        self.top = top
        self.skip = 0

    def __str__(self):
        """
        Returns human-readable string representation of query object.

        Returns:
            str: formatted new-lined list of query attributes

        Usage:
            query = Query("hello world", top=5, lang='en)
            print query -- > Lang: en
                             Skip: 0
                             Top: 5
                             Terms: hello world
                             Result_Type:

        """
        return '\n'.join(['{0}: {1}'.format(key.title(), value)
                          for (key, value) in self.__dict__.items()])

    def __eq__(self, other):
        """
        Overrides '==' operator, returns True if both querys hash to the same value.

        Usage:
            query = Query("hello world", top=30)
            query2 = Query("hello world")
            print query == query2 --> False

            query2.top = 30
            print query == query2 --> True

        """
        return hash(self) == hash(other)

    def __hash__(self):
        """
        Overrides hash() method, hashes tupled attributes of query.

        Returns:
            int: large unique integer, representing hashed value of query

        Usage:
            query = Query("court", top=25)
            print hash(query) --> 9160469348640922505

        """
        return hash(tuple(self.__dict__.items()))

    @staticmethod
    def check_input(input_string):
        """
        Takes a unicode string, encodes it to ascii
        whilst stripping out the punctuation.

        Returns cleaned string or None if string
        contains nothing/spaces.

        """
        PUNCTUATION = '!"#$%&\'()*+,-/;<=>?@[\\]^_`{|}~'

        # encode to ascii, ignoring non ascii chars
        s = input_string.encode('ascii', 'ignore')

        # remove all punctuation
        s = s.translate(string.maketrans(PUNCTUATION, ' '*len(PUNCTUATION)))

        # set to None if just spaces
        if s.isspace():
            s = None

        return s