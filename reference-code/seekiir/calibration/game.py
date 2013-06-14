__author__ = 'leif'

import os
import sys
from datetime import datetime

from terminal_colors import bcolors, print_warning, print_okblue, print_okgreen, print_fail
from calibration import settings
from django.core.management import setup_environ
setup_environ(settings)

from calibrate.models import TestCollection, Topic, Document

from screens import show_pause, show_topic_screen, show_instructions, splash_screen, show_break_screen
from screens import show_document_screen, show_snippet_screen, show_options
from screens import progress, set_progress_topic, set_progress_doc
from event_logger import setup_event_logger, log_event

el = setup_event_logger('test.log', os.getcwd())

def filter_input(state):
    """ (int) --> (int)
    """
    show_options(state)
    outcomes = {0: ['s'],
                1: ['v','n'],
                2: ['r','n','u'],
                }
    ri = raw_input()

    ri = ri.lower()
    if len(ri) > 1:
        ri = ri[0]
    o = outcomes[state]

    if ri in o:
        return ri
    else:
        return 'x'


def log_action(event_logger, text_type, topic, doc, outcome, seconds):
    actions = {'s':'VIEW_SNIPPET', 'v':'VIEW_DOC', 'n':'SKIP_DOC', 'r':'DOC_REL', 'n':'DOC_NOTREL', 'u':'DOC_UNSURE'}
    a = 'ERR'
    if outcome in actions:
        a = actions[outcome]
    tt = 'SNIP'
    c = len(doc.snippet)
    l = len( doc.snippet.split(' '))
    if text_type == 1:
        tt = 'DOC'
        c = len(doc.text)
        l = len( doc.text.split(' '))
        
    log_event(event_logger, topic.num,tt, doc.docid, doc.relevant, c, l, a, seconds )


def process_document(ti, dj):
    """(topic,document) -> None
    """
    state = 1
    outcome = 'x'
    FMT = "%H:%M:%S,%f"
    #((datetime.strptime(vals[1],self.FMT)-datetime.strptime(self.last_event_time,self.FMT)) )
    last_time = datetime.now()
    # record time to look at snippet
    log_action(el, 0,ti,dj,'s',0.0)
    show_snippet_screen(ti,dj)
    while outcome == 'x':
        
        outcome = filter_input(state)
        # record time examining snippet
        if outcome =='x':
            show_pause('Command not found - try again!')
            log_action(el, 0,ti,dj,outcome,0.0)
    diff = (datetime.now() - last_time).total_seconds()
    last_time = datetime.now()
    
    log_action(el, 0,ti,dj,outcome,diff)

    if outcome == 'v':
        # record time of document viewed --
        state = 2
        outcome = 'x'
        show_document_screen(ti,dj)

        while outcome == 'x':
            outcome = filter_input(state)
            if outcome =='x':
                show_pause('Command not found - try again!')
                log_action(el, 1, ti,dj,outcome,0.0)
                
        diff = (datetime.now() - last_time).total_seconds()
        last_time = datetime.now()    
        log_action(el, 1,ti,dj,outcome,diff)
            
        # record time and judgement made by user (r,n,u)
    

def main():
    
    sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=100, cols=100))
    splash_screen()
    show_pause()
    show_instructions()
    show_pause()
    
    tc = TestCollection.objects.all()
    for coll in tc:
        t = Topic.objects.filter(testcollection=coll)
        for ti in t:
            d = Document.objects.filter(topic=ti)
            i = 0
            n = len(d)
            set_progress_doc(i,n)
            show_topic_screen(ti)
            show_pause()
            for dj in d:
                i += 1
                set_progress_doc(i)
                process_document(ti,dj)
            show_break_screen('Topic Completed.')
            show_pause()

if __name__ == '__main__':
    import doctest
    if doctest.testmod().failed:
        import sys
        sys.exit(1)
    main()

