__author__ = 'rose'
"""
This script generates the config files for page calculator experiments
config file looks like:
[experiment]
url = https://www.gov.uk/driving-a-minibus
engine = govuk
key=
domain=
cutoff=
maxqueries = 50
stopfile = stopwords.txt
cache = True
query_type = biterm
doc_portion_perc = 100
doc_portion_count =
selection_type = position
rank_type = odds
crawl_file =
divs= wrapper
"""
import os, sys
import ConfigParser

parts = ["all","main"]
portions = ['100','75','50','25']
rankings = ["ranked","position_ranked","position"]
max_queries = ['25','50','75']
urls = ["https://www.gov.uk/vehicles-you-can-drive", "https://www.gov.uk/youth-crime-prevention-programmes","https://www.gov.uk/apply-for-student-finance"]
engines = ["govuk","bing","sitebing"]
bing_key = "D3KxWY+hGljThaf/hVXqjMC21FThDjF0TP5xLHH3rhU"
domain = "gov.uk"
stopfile= "stopwords.txt"
rank_type = "odds"
top_path="results"
crawl_file="crawl.txt"
divs = "wrapper"
config = ConfigParser.ConfigParser()
# set a number of parameters

def set_config():


    config.add_section("experiment")
    for url in urls:
            for part in parts:
                for portion in portions:
                    for rank in rankings:
                        for max_query in max_queries:
                            for engine in engines:
                                directory = top_path + "/" + part + "/" + portion + "/" + rank + "/" + max_query + "/"
                                #print directory
                                #if not os.path.exists(directory):
                                #    os.makedirs(directory)
                                config.set("experiment", "url", url)
                                if engine == 'binguk' or engine == 'bing':
                                    config.set("experiment","key",bing_key)
                                config.set("experiment", "engine",engine)
                                if engine == 'sitebing':
                                    config.set("experiment","domain",domain)
                                config.set("experiment","maxqueries",max_query)
                                config.set("experiment","stopfile",stopfile)
                                config.set("experiment","query_type","biterm")
                                config.set("experiment","doc_portion_perc", portion)
                                config.set("experiment","selection_type",rank)
                                if rank == "ranked" or rank == "position_ranked":
                                    config.set("experiment","rank_type",rank_type)
                                    config.set("experiment","crawl_file",crawl_file)
                                if rank == "position_ranked" or rank == "position":
                                    config.set("experiment","divs",divs)
                                #config.write(sys.stdout)
                                if not os.path.exists(directory):
                                    os.makedirs(directory)
                                directory += "experiment_"+engine+".ini"
                                with open(directory, "w") as config_file:
                                    config.write(config_file)
                                reset()


def reset():
    """
    to clear the config of values which aren't always set such as rank type crawl file and key
    :return:
    """
    config.remove_option("experiment","key")
    config.remove_option("experiment","domain")
    config.remove_option("experiment","rank_type")
    config.remove_option("experiment","crawl_file")
    config.remove_option("experiment","divs")


set_config()