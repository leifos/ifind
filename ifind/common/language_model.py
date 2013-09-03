__author__ = 'rose'

class LanguageModel():
    """
    manages reading in a file and splitting into a term, occurrence dictionary
    or takes a term, occurrence dictionary
    calcuates the probability of a term occuring given the occurrence dict
    """
    def __init__(self, file=None , dict=None):
        self.occurrence_dict = {}
        self.TOTAL_OCCURRENCES = 0

        if file:
            self.populate_occurrences(file)
        else:
            self.occurrence_dict = dict

        self.__calc_total_occurrences()


    def populate_occurrences(self, file_name):
        """
        reads in a file and stores in occurrences dictionary
        :param fileName
        """
        if file_name:
            f = open(file_name, 'r')
            for line in f:
                split_line=line.split()
                term = split_line[0]
                #TODO need to make robust for errors in input file
                count = int(split_line[1])
                self.occurrence_dict[term] = count

    def __calc_total_occurrences(self):
        """
        counts the total number of term occurrences in occurrence_dict
        """
        for term, count in self.occurrence_dict.items():
            self.TOTAL_OCCURRENCES += count

    def get_total_occurrences(self):
        return self.TOTAL_OCCURRENCES

    def get_num_occurrences(self,term):
        """
        :param term: the individual term for which count is desired
        :return: number of occurrences for term in occurrence dict
        """
        return self.occurrence_dict[term]


    def get_term_probability(self, term):
        """
        calculates the probability of a term
        :param term:
        :return:
        """
        #todo add in rounding?
        return float(self.get_num_occurrences(term))/float(self.get_total_occurrences())


