__author__ = 'leif'



class QueryRanker(object):


    def __init__(self):
        self.crawl_dict() = {}

    def stat_based_query_generation(self, crawl_file, k, l=0.5):
        """
        takes in name of file with term, occurrences pairs crawled from website
        and uses this to calculate probabilities for each query which is sorted
        in descending order and the top k queries returned
        :param crawl_file: the file with terms and occurrences
        :param k: integer indicating the number of queries to be returned
        :param l : lambda, a parameter between 0 and 1 default 0.5
        :return:a list of k prioritised queries
        """
        pass

    def populate_crawl_dict(self, crawl_file):
        """
        reads in crawlFile and stores in dictionary which is returned
        :param crawl_file:
        :return:
        """
        if crawl_file:
            f = open(crawl_file, 'r')
            for line in f:
                split_line=line.split()
                term = split_line[0]
                #TODO need to make robust for errors in input file
                count = int(split_line[1])
                self.crawl_dict[term]=count

    def calculate_term_probability(self):
        pass

    def calculate_query_probability(self):
        pass

    def get_times_in_doc(self,term):
        pass

    def get_length_of_doc(self):
        pass

    def get_times_in_crawlfile(self,term):
    #get the number of times a term occurred in the crawl dictionary
        if self.crawl_dict:
            return self.crawl_dict[term]

    def get_total_crawl_occurrences(self):
        #get the total number of term occurences in the crawl dictionary
        #i.e. the sum of the values
        if self.crawl_dict:
            total = 0
            for term, value in self.crawl_dict.items():
                total += value
        return total