__author__ = 'leif'
from utils import run_queries

import sys



def main(query_filename,out_filename):
    """

    :param query_filename: list of queries, one per line
    :return: NONE

    Saves a json object containing a list of all the snippets to the out_filename

    Assume that for each query 10 results snippets per query.
    """

   # with open(query_filename, "r+") as fquery:
   #     for line in fquery:
   #         print line
   #list = run_queries(query_filename)
   #save_result_list(list,out_filename)





def usage(script_name):
    """
    Prints the usage message to the output stream.
    """
    print "Usage: {0} [query_filename] [out_filename]".format(script_name)
    print "Expects a query_filename that contains one query per line"

if __name__ == '__main__':
    if len(sys.argv) < 3 or len(sys.argv) > 3:
        usage(sys.argv[0])
    else:
        main(sys.argv[1], sys.argv[2])