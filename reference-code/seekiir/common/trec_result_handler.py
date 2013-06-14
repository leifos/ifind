__author__ = 'leifos'


from common.common_helpers import file_exists
from common.common_helpers import AutoVivification
from common.topic_document_file_handler import TopicDocumentFileHandler


def process_trec_line(line):
# handles the specific format of the line - assumes 6 columns TREC Result format
	# topic QO document rank score EXP
	parts = line.partition(' ')
	topic = parts[0]
	parts = parts[2].partition(' ')
	parts = parts[2].partition(' ')
	doc = parts[0]
	parts = parts[2].partition(' ')
	rank = parts[0]
	parts = parts[2].partition(' ')
	score = parts[0]

	return (topic, doc, rank, score)


class TrecResultHandler(TopicDocumentFileHandler):

    def __init__(self, filename=None):
        super(TrecResultHandler, self).__init__(filename)

    def _put_in_line(self, line):
        topic, doc, rank, score = process_trec_line(line)
        if topic and doc:
            self.data[topic][doc] =  (int(rank), float(score))

    def _get_out_line(self, topic, doc):
        # outputs in TREC Result format
        return "%s Q0 %s %d %f EXP\n" % (topic, doc.strip(), self.get_value(topic,doc), self.get_score(topic,doc))

    def get_score(self, topic, doc):
        if self.data[topic][doc]:
            return self.data[topic][doc][1]
        else:
            return 0.0

    def get_value(self, topic, doc):
        if self.data[topic][doc]:
            return self.data[topic][doc][0]
        else:
            return 0

    def get_rank(self, topic, doc):
        return self.get_value(topic, doc)


    def get_ranking(self, topic):
        '''
        Returns an ordered list of tuples (doc,rank, score)
        '''
        udl = self.get_doc_list(topic)
        dl = []
        for d in udl:
            dl.append((d, self.get_rank(topic,d), self.get_score(topic,d)))
        odl = sorted(dl, key=lambda doc: doc[1])

        return odl

    def save_file(self, filename, append=False):
        ''' Saves the docs ordered by rank for each topic
        '''
        if append:
            outfile = open(filename, "a")
        else:
            outfile = open(filename, "w")

        for t in self.get_topic_list():
            odl = self.get_ranking(t)
            for d in odl:
                out_line = self._get_out_line(t,d[0])
                outfile.write (out_line)

        outfile.close()

    def clear(self):
	    self.data = AutoVivification()
