__author__ = 'leif'


class RotationOrdering(object):
    """ creates ordering for lists with an attribute id

    """
    def __init__(self):
        pass

    def number_of_orderings(self):
        return 1

    def get_ordering(self, list, i=0):
        """ given a list (i.e. of pages, cats), return the ith ordering

        :param list with and id:
        :param i:
        :return: list of ids
        """

        id_list = []
        for p in list:
            if p.id:
                id_list.append(p.id)
        #id_list = id_list[::-1]

        return id_list