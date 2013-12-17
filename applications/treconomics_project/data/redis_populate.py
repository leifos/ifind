__author__ = 'david'

import os
import sys
import redis
import timeit
from ifind.search.query import Query
from ifind.search.engines.whooshtrecnewsredis import WhooshTrecNewsRedis

#  Global settings
WORK_DIRECTORY = os.getcwd()
WHOOSH_DIRECTORY = os.path.join(WORK_DIRECTORY, 'fullindex')
QUERY_FILENAME = 'redis_populate_queries.txt'
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
CACHE_UPTO_PAGE = 10

#  Redis and Engine objects
REDIS_CONNECTION = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)
ENGINE = WhooshTrecNewsRedis(whoosh_index_dir=WHOOSH_DIRECTORY, cache_host=REDIS_HOST, cache_port=REDIS_PORT)

def main(argv):
    """
    The script's main function, called the script is started.
    """
    argv_len = len(argv)

    #  Is the Redis server working?
    try:
        REDIS_CONNECTION.client_list()
    except redis.ConnectionError:
        print "ERROR: Couldn't communicate with Redis server @ {0}:{1}. Check settings?".format(REDIS_HOST, REDIS_PORT)
        return 1

    #  Need a minimum number of arguments
    if argv_len < 2:
        print_usage(argv)
        return 1

    #  The main conditional blocks - if we pass these, a bad combination of options was supplied.
    if argv[1] == 'parse' and argv_len == 3:
        parse_file(argv[2])
        return 0
    elif argv[1] == 'cache' and argv_len == 2:
        cache_queries()
        return 0
    elif argv[1] == 'flush' and argv_len == 2:
        REDIS_CONNECTION.flushall()
        print "Cache flushed."
        return 0

    print_usage(argv)
    return 1


def print_usage(argv):
    """
    Prints the script's usage to the terminal.
    """
    print "{0} Usage:".format(argv[0])
    print "  - {0} parse <FILENAME>.".format(argv[0])
    print "      Parse an input file (in TREC topic format) and append queries{0}" \
          "      found to {1}.".format(os.linesep, QUERY_FILENAME)
    print "  - {0} cache".format(argv[0])
    print "      Cache queries found in {0}.".format(QUERY_FILENAME)
    print "      Term results, query results and query results up to page {0}{1}" \
          "      will be cached.".format(CACHE_UPTO_PAGE, os.linesep)
    print "  - {0} flush".format(argv[0])
    print "      Flush the Redis cache at {0}:{1}.".format(REDIS_HOST, REDIS_PORT)


def parse_file(query_filename):
    """
    Taking a filename pointing to a file in TREC topic format, parses the file and appends queries to the file
    pointed to by QUERY_FILENAME. If a line is malformed, it is ignored.
    """
    input_file = open(query_filename, 'r')
    output_file = open(QUERY_FILENAME, 'a')
    queries_to_append = []

    for line in input_file:
        line = line.strip()
        line = line.lower()
        line = line.partition(' ')

        if len(line) == 3:
            line = line[2].strip()

            if line not in queries_to_append:
                queries_to_append.append(line)

    for query in queries_to_append:
        output_file.write("{0}{1}".format(query, os.linesep))

    input_file.close()
    output_file.close()
    print "File read complete."


def cache_queries():
    execution_time = timeit.default_timer()
    query_list = read_query_terms()

    for query in query_list:
        query_start_time = timeit.default_timer()
        print "-" * 80
        print "> {0}".format(query)

        query = Query(terms=query)
        query.top = 10
        query.skip = 300000000

        ENGINE.search(query)

        print "  >> Elapsed time: {0:.2f} second(s)".format(timeit.default_timer() - query_start_time)

    print "=" * 80
    print "> Total execution time: {0:.2f} seconds".format(timeit.default_timer() - execution_time)
    print "> Page caching thread will die shortly, or just kill the Python process."


def read_query_terms():
    """
    Reads in query terms, returning a list of unicode strings, with each string representing a query.
    """
    query_list = []
    file_obj = open(QUERY_FILENAME)

    for line in file_obj:
        line = line.strip()
        line = line.lower()
        line = unicode(line)

        if line not in query_list:
            query_list.append(line)

    file_obj.close()
    return query_list


if __name__ == '__main__':
    sys.exit(main(sys.argv))