__author__ = 'leif'

from ifind.search.query import Query


class SearchContext(object):

    def __init__(self, topic):
        self.Topic = topic
        self.Relevance = None
        self.Background = None
        self.UserQueryList = None


class Topic(object):

    def __init__(self, topic_text):
        self.text = topic_text




class Relevance(object):
    pass



class UserQuery(object):

    def __init__(self, query_text, query_score):
        self.text = query_text
        self.score = query_score
        self.issued = False
        self.exhausted = False
        self.pos_examined = 0



class UserQueryList(object):

    def __init__(self):
        self.ql = []

    def add_query(self, text, score):
        self.ql.append( UserQuery(text, score) )



    def get_next_query(self):
        """
        gets the query with the highest score, which has not been issued, and returns it
        :return: a UserQuery object
        """

        # sort list
        #TODO(leifos): need to ensure the list is sorted first

        n = len(self.ql)
        i = 0
        while (i < n):
            if self.ql[i].issued:
                i = i + 1
            else:
                break

        if i < n:
            return self.ql[i]
        else:
            return None
