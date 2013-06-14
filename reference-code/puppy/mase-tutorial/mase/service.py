import os, os.path

from puppy.service import ServiceManager, SearchService
from puppy.search.engine import BingV3, Twitter, YouTubeV2, Wikipedia
from puppy.search.engine.whooshQueryEngine import WhooshQueryEngine
from puppy.query.filter.whooshQueryLogger import WhooshQueryLogger
from puppy.logging import QueryLogger
from puppy.query.filter import BlackListFilter
from puppy.query.modifier import BlackListModifier


from settings import ONDOLLEMAN, DOLLEMANPATH

log_dir = "mase/query_logs"

if ONDOLLEMAN:
    whoosh_dir = os.path.join(DOLLEMANPATH, "mase/query_logs/index")
    log_dir = os.path.join(DOLLEMANPATH, log_dir)
else:
    whoosh_dir = os.path.join(os.getcwd(), "mase/query_logs/index")

config = {
 "proxyhost": "http://wwwcache.gla.ac.uk:8080", # <-- remove if not UGLW
 "log_dir": log_dir,
 "bing_api_key": "/aROdM5Ck7fKHR4ge30r8W/K/D84GJkcl42lL8eNMSc=",  # Obtain key from https://datamarket.azure.com/dataset/5BA839F1-12CE-4CCE-BF57-A49D98D29A44
}

# create a ServiceManager
service = ServiceManager(config)

# create a ServiceManager
service = ServiceManager(config)

# create a Web SearchService
web_search_service = SearchService(service, "web_search")
web_search_service.search_engine = BingV3(web_search_service, source='Web', resultsPerPage = 4)
service.add_search_service(web_search_service)

# Create a blacklist filter to block queries containing the terms below
query_black_list = BlackListModifier(terms = "bad worse nasty filthy")

#Add our blacklist filter to the web search service
web_search_service.add_query_modifier(query_black_list)# Add Web SearchService to ServiceManager


# create a file based QUERY LOGGER
web_search_service.query_logger = QueryLogger(web_search_service, log_mode=0)
web_search_service.postLogging = True

# create a index based QUERY LOGGER
whoosh_query_logger = WhooshQueryLogger(whoosh_query_index_dir=whoosh_dir, unique=True)
web_search_service.add_query_filter(whoosh_query_logger)



# create a SearchService, called 'query_suggest_search'
suggest_service = SearchService(service, "query_suggest_search")

# Use the Whoosh Query Engine to record queries
whooshEngine = WhooshQueryEngine(suggest_service, whoosh_query_index_dir=whoosh_dir)
suggest_service.search_engine = whooshEngine

# add SearchService to our ServiceManager
service.add_search_service(suggest_service)


# create a WIKIPEDIA SearchService and add to ServiceManager
wiki_search_service = SearchService(service, "wiki_search")
wiki_search_service.search_engine = Wikipedia(wiki_search_service, resultsPerPage = 4)
service.add_search_service(wiki_search_service)

# create a VIDEO SearchService and add to ServiceManager
video_search_service = SearchService(service, "video_search")
video_search_service.search_engine = YouTubeV2(video_search_service, resultsPerPage = 4)
service.add_search_service(video_search_service)


# create a NEWS SearchService and add to ServiceManager
news_search_service = SearchService(service, "news_search")
news_search_service.search_engine = BingV3(news_search_service, source='News', resultsPerPage = 4)
service.add_search_service(news_search_service)


# create a IMAGE SearchService and add to ServiceManager
image_search_service = SearchService(service, "image_search")
image_search_service.search_engine = BingV3(image_search_service, source='Image', resultsPerPage = 12)
service.add_search_service(image_search_service)


# create a TWITTER SearchService and add to ServiceManager
twitter_search_service = SearchService(service, "twitter_search")
twitter_search_service.search_engine = Twitter(twitter_search_service, resultsPerPage = 5)
service.add_search_service(twitter_search_service)

