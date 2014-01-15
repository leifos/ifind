__author__ = 'rose'
"""
this script aims to create a folder with a structure to reflect all the possible combinations
for the results files for the page calculator experiments
"""

#!/usr/bin/python

import os, sys

# Path to be created
top_path = "results"
scoring = ["cumulative","gravity"]
parts = ["all","main"]
portions = ['100','75','50','25']
rankings = ["ranked","unranked"]
max_queries = ['25','50','75','all']
previous = ['']
directory = ''
for score in scoring:
    for part in parts:
        for portion in portions:
            for rank in rankings:
                for max_query in max_queries:
                    directory = top_path + "/" + score + "/" + part + "/" + portion + "/" + rank + "/" + max_query + "/"
                    #print directory
                    if not os.path.exists(directory):
                        os.makedirs(directory)


print "Directories are created"