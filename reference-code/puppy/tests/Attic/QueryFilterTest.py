#!/usr/bin/python
# -*- coding: utf-8 -*-

from puppy.service import Service
from puppy.search import SearchEngine
from puppy.query.filter import TermExpansionFilter
from puppy.query.filter import BlackListFilter
from puppy.query.filter import TestEqualFilter

from puppy.model import Query




service = Service()

black_list_query = "--terms=+book"


service.add_query_filter(TermExpansionFilter("--terms=for+kids"))
service.add_query_filter(TestEqualFilter("--terms=for+kids+elmo"))
service.add_query_filter(TermExpansionFilter("--terms=colouring+book"))
service.add_query_filter(TestEqualFilter("--terms=for+kids+elmo+colouring+book"))
service.add_query_filter(BlackListFilter("--terms=+book"))

# This line fails, book is not longer in  the query list
#service.add_query_filter(TestEqualFilter("--terms=for+kids+elmo+colouring+book"))

service.add_search_engine(SearchEngine('Yahoo'))


query = Query('elmo')
service.search(query)

