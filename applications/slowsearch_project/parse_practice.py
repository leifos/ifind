from datetime import datetime, timedelta
import time


logFile = open('experiment.log', 'r')

FILE = logFile.readlines()

logFile.close()

time_list = []
query_time = ""
response_time = ""
queries = 0

for line in FILE:
    if 'PA' in line:
        print line





