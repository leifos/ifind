from ifind.common.page_retrievability_calc import PageRetrievabilityCalculator
from ifind.common.query_generation import BiTermQueryGeneration
from ifind.search.engine import EngineFactory

# words to exclude from query
STOPWORD_FILE = "stopwords.txt"
# urls to be calculated
URL_FILE = "findability.txt"
# result output
RESULT_FILE = "retrievability.txt"

# minimum query term length
TERM_LEN = 3

# retrievability cutoff
CUTOFF = 10


def get_trending_queries(filename):
    with open(filename, 'r') as f:
        return [tuple((line.strip()).split(',')) for line in f]


def main():
   
    engine = EngineFactory(engine='Sitebing',
                           api_key="",
                           throttle=0.1,
                           cache='engine')

    query_generator = BiTermQueryGeneration(minlen=TERM_LEN, stopwordfile=STOPWORD_FILE, maxsize=200)
    tuple_list = get_trending_queries(URL_FILE)
    page_calculator = PageRetrievabilityCalculator(engine=engine, cutoff=CUTOFF, generator=query_generator)

    with open(RESULT_FILE, 'a') as f:

        for tuple in tuple_list:
            url = tuple[1]
            findability = tuple[0]
            category_name = tuple[2]
            retrievability = page_calculator.score_page(url)
            s = page_calculator.stats()

            f.write('{0},{1},{2},{3},{4},{5},{6}\n'.format(category_name,
                                                           url,
                                                           findability,
                                                           retrievability,
                                                           s['retrieved'],
                                                           s['query_count']))

if __name__ == "__main__":
    main()