__author__ = 'rose'

class LanguageModel():
    """
    manages reading in a file and splitting into a term, occurrence dictionary
    or takes a term, occurrence dictionary
    calculates the probability of a term occurring given the occurrence dict
    """

    #TODO(leifos): dict is a reserved word - i.e. defines a dict.. be mindful of using dict, list, etc unless you are creating one.
    def __init__(self, file=None , occurrences_dict=None):
        self.occurrence_dict = {}
        self.TOTAL_OCCURRENCES = 0

        if file:
            self._populate_occurrences(file)
        else:
            self.occurrence_dict = occurrences_dict

        self._calc_total_occurrences()


    def _populate_occurrences(self, file_name):
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

    def _calc_total_occurrences(self):
        """
        counts the total number of term occurrences in occurrence_dict
        """
        for term, count in self.occurrence_dict.items():
            self.TOTAL_OCCURRENCES += count

    def get_total_occurrences(self):
        return self.TOTAL_OCCURRENCES

    #TODO(leifos): be consisent, this was get_number_terms.. it was used as get_num_terms
    def get_num_terms(self):
        return len(self.occurrence_dict)

    def get_num_occurrences(self,term):
        """
        :param term: the individual term for which count is desired
        :return: number of occurrences for term in occurrence dict, 0 if not in
        """
        if term in self.occurrence_dict:
            return self.occurrence_dict[term]
        else:
            return 0

    def get_term_prob(self, term):
        """
        calculates the probability of a term
        :param term:
        :return:
        """
        if self.get_num_occurrences(term) == 0:
            return 0
        else:
            result =float(self.get_num_occurrences(term))/float(self.get_total_occurrences())
            result = round(result,2)
            return result


