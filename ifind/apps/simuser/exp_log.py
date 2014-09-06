__author__ = 'leif'


class ExpLog(object):

    def __init__(self, limit=300):
        self.qc = 10
        self.dc = 20
        self.sc = 3
        self.rpc = 5
        self.md = 3
        self.total_time = 0
        self.limit = limit



    def log_action(self, action_name):
        action_mapping = {
            'QUERY': self.log_query,
            'SERP': self.log_serp,
            'SNIPPET': self.log_snippet,
            'DOC': self.log_assess,
            'MARK': self.log_mark_document
        }

        if action_mapping[action_name]:
            action_mapping[action_name]()
        else:
            self.log_unknown_action(action_name)


    def log_unknown_action(self):
        self.report('U')

    def log_query(self):
        self.total_time += self.qc
        self.report('Q')


    def log_assess(self):
        self.total_time += self.dc
        self.report('D')

    def log_snippet(self):
        self.total_time += self.sc
        self.report('S')

    def log_serp(self):
        self.total_time += self.rpc
        self.report('R')

    def log_mark_document(self):
        self.total_time += self.md
        self.report('M')

    def is_finished(self):
        return (self.total_time < self.limit)


    def report(self, action):
        print self.limit, self.total_time, action


