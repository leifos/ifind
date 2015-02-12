from xml.dom import minidom 
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.analysis import StemmingAnalyzer
import os

stemmer = StemmingAnalyzer()
schema = Schema(docid=TEXT(stored=True), title=TEXT(analyzer=stemmer, stored=True), content=TEXT(analyzer=stemmer, stored=True),
                timedate=TEXT(stored=True), source=TEXT(stored=True), alltext=TEXT(stored=True) )


work_dir = os.getcwd()
my_whoosh_doc_index_dir = os.path.join(work_dir, 'test100index')
xml_files = os.path.join(work_dir,'aquaint_xml.files')

ix = create_in(my_whoosh_doc_index_dir, schema)

doc_list_file = os.path.join(work_dir,'qrel.uniq.docids')


def readDataFiles( datafile ):
    filelist = []
    f = open(datafile,"rb")
    for line in f.readlines():
        filelist.append(line.rstrip())
        #print line
    f.close()
    return filelist

def getText(nodelist):
    rc = [u'']
    for nl in nodelist:
        if nl.firstChild:
            rc.append(nl.firstChild.data)
    return u''.join(rc)
    
files_to_process = readDataFiles(xml_files)   
doc_list = readDataFiles(doc_list_file)


writer = ix.writer(limitmb=2048, procs=1, multisegment=False)
for dfile in files_to_process:        
    print "processing file: " + dfile
    xmldoc = minidom.parse( dfile)
    for node in xmldoc.getElementsByTagName("DOC"):
        tmp = node.getElementsByTagName('DOCNO')
        ndocid = getText(tmp)
        ndocid = ndocid.strip() 
        
        if ndocid in doc_list:
            print "Processing: *"+ndocid+"*"
            tmp = node.getElementsByTagName('HEADLINE')
            ntitle = getText(tmp)
            
            textnode = node.getElementsByTagName('TEXT')
            ncontent = getText(textnode)
            ptext = ""
            for pnode in textnode[0].getElementsByTagName('P'):
                ptext = ptext + "<p>" + pnode.firstChild.data + "</p>" 
            
            
            ncontent = ncontent + " " +  ptext
            tmp = node.getElementsByTagName('DATE_TIME')
            ntimedate = getText(tmp)
            print ndocid
            nsource = u""
            
            if ndocid.startswith('APW'):
                nsource = u"Associated Press Worldwide News Service"
            if ndocid.startswith('XIE'):
                nsource = u"Xinhua News Service"
            if ndocid.startswith('NYT'):
                nsource = u"New York Times News Service"

            nalltext = ntitle + " " + ncontent + " " + nsource
            
            #check if the docid is on the list of docs to be 
            writer.add_document(docid=ndocid, title=ntitle, content=ncontent, timedate=ntimedate, source=nsource, alltext=nalltext)
        else:
            print "Skipping: *"+ndocid+"*"
writer.commit()

