import urllib2


class sitesearch(object):
    def __init__(self, sites):
        self.sites = sites

    def _modify_query(self, query):
        if self.sites:
            query = query + ' (' + ' OR '.join('site:%s' % site for site in
                    self.sites) + ')'

        return query
