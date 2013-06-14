#!/usr/bin/python
# -*- coding: utf-8 -*-

from puppy.service import Service
from puppy.search import SearchEngine
from puppy.query.filter import TermExpansionFilter
from puppy.result.filter import BlackListResultFilter
from puppy.result.filter import ExclusionFilter
from puppy.model import Query


service = Service()

black_list_result = "--terms=verybadword"
exclusion_list_result = "--terms=badword"


service.add_search_engine(SearchEngine('EchoSearch'))

service.add_result_filter(ExclusionFilter(exclusion_list_result))

service.add_result_filter(BlackListResultFilter(black_list_result))


query = Query('elmo badword verybadword')
service.search(query)

