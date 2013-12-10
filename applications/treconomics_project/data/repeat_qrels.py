class AutoVivification(dict):
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

def ReadQrelsFile(qrel_file):
    qrels = AutoVivification()

    infile = open( qrel_file, "r" )
    while infile:
        line = infile.readline()
        #print line
        parts = line.partition(' ')
        query_num = parts[0]
        parts = parts[2].partition(' ')
        parts = parts[2].partition(' ')
        doc_num = parts[0]
        judgement = '0' + parts[2].strip()
        
        
        qrels[query_num][doc_num] =  int(judgement)
        
        if not line:
            break
            
    return qrels

qrel_file = "/Users/leif/Code/ifind/applications/treconomics_project/data/trec2005.qrels.435"

qrels = ReadQrelsFile( qrel_file )

topic_num = '435'

q = 237

for i in range(q):
    for doc in qrels[topic_num]:
        x = topic_num +"-"+str(i) + " Q0 " + doc + " " + str(qrels[topic_num][doc])
        print x.strip()