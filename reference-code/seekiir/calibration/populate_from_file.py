__author__ = 'kojayboy'
from calibration import settings
from django.core.management import setup_environ
setup_environ(settings)
from calibrate.models import TestCollection, Topic, Document
from HTMLParser import HTMLParser
from re import sub
import sys
import codecs
from traceback import print_exc

class _DeHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.__text = []
    
    def handle_data(self, data):
        text = data.strip()
        if len(text) > 0:
            text = sub('[ \t\r\n]+', ' ', text)
            self.__text.append(text + ' ')
    
    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.__text.append('\n\n')
        elif tag == 'br':
            self.__text.append('\n')
    
    def handle_startendtag(self, tag, attrs):
        if tag == 'br':
            self.__text.append('\n\n')
    
    def text(self):
        return ''.join(self.__text).strip()


def dehtml(text):
    try:
        parser = _DeHTMLParser()
        parser.feed(text)
        parser.close()
        return parser.text()
    except:
        print_exc(file=stderr)
        return text

TestCollection.objects.all().delete()
Topic.objects.all().delete()
Document.objects.all().delete()

tca = TestCollection(name='Aquaint', type='News')
tca.save()
tcb = TestCollection(name='TREC123', type='News')
tcb.save()
tcc = TestCollection(name='WT10G', type='Web')
tcc.save()
tcd = TestCollection(name='DotGov', type='Web')
tcd.save()

tc = TestCollection.objects.all()
for i in tc:
    print i

doc_file = open('data/document_file_list.txt')
for doc_line in doc_file:
    topic_no = doc_line.strip()
    result_file=codecs.open('data/' + topic_no + '.documents', encoding='Latin-1')
    relevancy_file=open('data/' + topic_no + '.relevancy')
    topic_file = open('data/' + topic_no + '.qry')
    docmap = {}
    for line2 in relevancy_file:
        split_line = line2.split()
        docmap[split_line[0]] = split_line[1]
    
    in_query = False
    in_desc = False
    in_narr = False
    query_line = ''
    desc_line = ''
    narr_line = ''
    queryNum = ''
    for line3 in topic_file:
        if "<title>" in line3:
            query_line = line3[8:].strip()
            in_query = True
            continue
        elif "<desc>" in line3:
            in_query = False
            in_desc = True
        elif "<narr>" in line3:
            in_desc = False
            in_narr = True
        elif in_query:
            query_line = query_line + line3
            continue
        elif in_desc:
            desc_line = desc_line + line3
            continue
        elif in_narr:
            narr_line = narr_line + line3
            continue

    collection = ''

    if int(topic_no) < 201:
        collection = tcb
    elif int(topic_no) < 401 and int(topic_no) > 300:
        collection = tca
    elif int(topic_no) < 601 and int(topic_no) > 550:
        collection = tcd
    elif int(topic_no) < 551 and int(topic_no) > 450:
        collection = tcc
    
    t = Topic(testcollection=collection, num=topic_no, title=query_line, summary=desc_line, desc=narr_line)
    t.save()
    
    indoc = False
    skip = 0
    in_docno = False
    in_title= False
    in_head = False
    in_headline = False
    in_hl = False
    document = ''
    docno = ''
    title = ''
    for line in result_file:
        if '<doc>' in line.lower():
            indoc = True
            continue
        elif '</doc>' in line.lower():
            parsed_document = dehtml(document)
            relevancy_score = docmap.get(docno)
            if not relevancy_score: ## Because TREC sucks and didn't retrieve the same pool of docs we do
                relevancy_score = 0
            docid = docno[(docno.lower()).find("<docno>")+7:(docno.lower()).find("</docno>")].strip()

            if (collection == tcc or collection == tcd):
                tit = title[(title.lower()).find("<title>")+7:(title.lower()).find("</title>")].strip()
            elif (collection == tca or collection == tcb) and '<headline>' in title.lower():
                tit = title[(title.lower()).find("<headline>")+10:(title.lower()).find("</headline>")].strip()
            elif (collection == tca or collection == tcb) and '<head>' in title.lower():
                tit = title[(title.lower()).find("<head>")+6:(title.lower()).find("</head>")].strip()
            elif (collection == tca or collection == tcb) and '<hl>' in title.lower():
                tit = title[(title.lower()).find("<hl>")+4:(title.lower()).find("</hl>")].strip()

            parsed_title = dehtml(tit)

            Document(topic=t, docid=docid, title=parsed_title, text=parsed_document, snippet=parsed_document[50:200], relevant=relevancy_score).save()

            indoc = False
            document = ''
            title = ''
            tit = ''
            parsed_title = ''
            parsed_document = ''
            docno = ''
            continue
                
        if '<docno>' in line.lower() and '</docno>' in line.lower():
            docno = line
            continue
        elif '<docno>' in line.lower() and '</docno>' not in line.lower():
            docno = line
            in_docno = True
            continue
        elif '<docno>' not in line.lower() and '</docno>' in line.lower():
            docno = docno + line
            in_docno = False
            continue
        elif in_docno:
            docno = docno + line
            continue


        if '<title>' in line.lower() and '</title>' in line.lower() and (collection == tcc or collection == tcd):
            title = line
            continue
        elif '<title>' in line.lower() and '</title>' not in line.lower() and (collection == tcc or collection == tcd):
            title = line
            in_title = True
            continue
        elif '<title>' not in line.lower() and '</title>' in line.lower() and (collection == tcc or collection == tcd):
            title = title + line
            in_title = False
            continue
        elif in_title:
            title = title + line
            continue

        if '<headline>' in line.lower() and '</headline>' in line.lower() and (collection == tca or collection == tcb):
            title = line
            continue
        elif '<headline>' in line.lower() and '</headline>' not in line.lower() and (collection == tca or collection == tcb):
            title = line
            in_headline = True
            continue
        elif '<headline>' not in line.lower() and '</headline>' in line.lower() and (collection == tca or collection == tcb):
            title = title + line
            in_headline = False
            continue
        elif in_headline:
            title = title + line
            continue

        if '<head>' in line.lower() and '</head>' in line.lower() and (collection == tca or collection == tcb):
            title = line
            continue
        elif '<head>' in line.lower() and '</head>' not in line.lower() and (collection == tca or collection == tcb):
            title = line
            in_head = True
            continue
        elif '<head>' not in line.lower() and '</head>' in line.lower() and (collection == tca or collection == tcb):
            title = title + line
            in_head = False
            continue
        elif in_head:
            title = title + line
            continue

        if '<hl>' in line.lower() and '</hl>' in line.lower() and (collection == tca or collection == tcb):
            title = line
            continue
        elif '<hl>' in line.lower() and '</hl>' not in line.lower() and (collection == tca or collection == tcb):
            title = line
            in_hl = True
            continue
        elif '<hl>' not in line.lower() and '</hl>' in line.lower() and (collection == tca or collection == tcb):
            title = title + line
            in_hl = False
            continue
        elif in_hl:
            title = title + line
            continue


        if '<dochdr>' in line.lower():
            skip = skip + 1
        if '</dochdr>' in line.lower():
            skip = skip - 1
#        if '<!--' in line.lower():
#            skip = skip + 1
#        if '-->' in line.lower():
#            skip = skip - 1
        if '<style>' in line.lower():
            skip = skip + 1
        if '</style>' in line.lower():
            skip = skip - 1
        if indoc and skip < 1:
            document = document + line

t = Topic.objects.all()
for i in t:
    print i

d = Document.objects.all()
for i in d:
    print i
