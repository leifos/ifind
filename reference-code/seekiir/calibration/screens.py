from terminal_colors import bcolors, print_warning, print_okblue, print_okgreen, print_fail
import os

WIDTH = 100
PAGINATE = 30


progress = { 'ti':0, 'tn':0, 'di':0, 'dn':0 }

def set_progress_topic(i,n=None):
    progress['ti'] = i
    if n:
        progress['tn'] = n

def set_progress_doc(i,n=None):
    progress['di'] = i
    if n:
        progress['dn'] = n


def count_line_breaks(text):
    """ (string)--> (int)
    Takes a string of text and counts the number of "\n" characters that appear in the text.
    >>> count_line_breaks("hello\\nsworld")
    1
    >>> count_line_breaks("hello\\nsorld\\n")
    2
    >>> count_line_breaks('jello dorld')
    0
    >>> count_line_breaks('kello eorld\\n')
    1
    """
    broken_text = text.split('\n')
    return len(broken_text)-1


def format_text_width(text, width):
    """ (string,int) --> (string)
    Takes a string of text and inserts carriage returns "\n" within the string at a space before the maximum width.
    Replacing spaces with "\n" when inserting
    
    >>> format_text_width('rello dorld',11)
    'rello dorld'

    >>> format_text_width('wello jorld',11)
    'wello jorld'
    
    >>> s = format_text_width('wello jorld',6)
    >>> print s
    wello
    jorld
    
    >>> s = format_text_width('hello\\nworld good bye world',11)
    >>> print s
    hello
    world good
    bye world
    
    >>> s = format_text_width('wellojorld',6)
    >>> print s
    wello-
    jorld
    
    """
    lines = ''
    n = len(text)
    
    while n > width:
        br = text.rfind('\n',0,width)
        if br > 0:
            lines = lines + text[0:br+1]
            new_text = text[br+1:n]
        else:
            i = width
            while (text[i] != ' ') and (i > 0):
                i = i - 1
            
            if i == 0:
                lines = lines + text[0:width-1]+'-\n'
                new_text = text[width-1:n]
            else:
                lines = lines + text[0:i]+'\n'
                new_text = text[i+1:n]
                
        text = new_text
        n = len(text)
        
    if n <= width:
        lines = lines + text
        
    return lines


def center_text(text,width):
    n = len(text)
    if n > width:
        return text
    else:
        
        padding = (width-n) / 2
        return (' ' * padding ) + text



def show_title():
    show_line(WIDTH)
    print(center_text('Document Assessment Utility',WIDTH))
    show_line(WIDTH)

def show_instructions():
    cls_screen()
    show_title()
    show_break(1)
    text = 'Imagine that you are using a search engine and are reading through the results for a query for a given topic.\n\n'
    print format_text_width(text, WIDTH)
    
    text = 'You will be shown the search topic which describes what is relevant and what is not. We will then show you a series of snippets, one at a time.\n\n'
    print format_text_width(text, WIDTH)
    
    text = 'Please read through each snippet, and decide to either view the full document to decide if it is relevant or skip to the next snippet. When you view a document read through it and then decide whether you think it is relevant, not relevant, or if you are unsure about its relevance.\n\n'
    print format_text_width(text, WIDTH)
    
    text = 'For each topic you will be asked to look through about 20 snippets/documents. And we have about 6 topics for you to examine.\n\nThank you for your time.'
    print format_text_width(text, WIDTH)
    
    show_line(WIDTH)
    show_break(1)

def splash_screen():
    cls_screen()
    show_line(WIDTH)
    show_break(10)
    print(center_text('Document Assessment Utility',WIDTH))
    show_break(10)
    show_line(WIDTH)
    show_break(1)

def cls_screen():
    os.system('clear')

def show_line(width):
    """ (int) --> None
    prints out -'s the size of width
    >>> show_line(5)
    -----
    """
    print '-'*width

def show_break(depth):
    for i in range(depth):
        print ''

def show_topic(topic, summary=False):
    """ (Topic, int)--> None """
    topic_line = topic.num + ' ' + topic.title
    print(format_text_width(topic_line, WIDTH))
    if summary:
        print(format_text_width(topic.summary, WIDTH))
    else:
        print(format_text_width(topic.desc, WIDTH))

def show_topic_summary(topic):
    """ (Topic)--> None """
    show_topic(topic, True)
    
def show_snippet(document):
    """ (Document) --> None """
    print_okblue(document.title)
    print_okblue('-'*len(document.title))
    print format_text_width(document.snippet,WIDTH)

def paginate(text, num_lines):
    """ (string, int) --> None
    Puts a show_pause() between num_lines in the text.
       
    """
    broken_text = text.split('\n')
    n  = len(broken_text)-1

    while (n > num_lines):
        for i in range(num_lines):
             print broken_text[i]
        del broken_text[0:num_lines]
        n = len(broken_text)-1
        show_break(1)
        show_pause()
    
    if n > 0:
        for i in range(n):
            print broken_text[i]

def show_document(document):
    """ (Document) -> None    """

    print_okblue(document.title)
    print_okblue('-'*len(document.title))
    text = format_text_width(document.text,WIDTH)
    paginate(text,PAGINATE)
    show_break(1)


def show_options(state):
    """ (int) -> None
    """
    options = { 0: '(S)tart',
                1: '(V)iew (N)ext',
                2: '(R)elevant (N)ot Relevant (U)nsure',
    }

    print_okblue(center_text(options[state],WIDTH))


def show_progress():
    print 'You are on document no. %d out of %d' % (progress['di'],progress['dn'])


def show_break_screen(msg):
    cls_screen()
    show_title()
    for i in range(10):
        print ' '
    text = '\t\t' + msg
    print_warning(text)
    for i in range(10):
        print ' '   
    show_line(WIDTH)

def show_topic_screen(topic):
    cls_screen()
    show_title()
    show_break(1)
    show_topic(topic)
    show_line(WIDTH)
    show_break(1)

def show_snippet_screen(topic, document):
    cls_screen()
    show_title()
    show_break(1)
    show_topic_summary(topic)
    show_break(1)
    show_progress()
    show_line(WIDTH)
    show_break(1)
    show_snippet(document)
    show_break(1)
    show_line(WIDTH)
    show_break(1)

def show_pause(reason=None):
    if reason:
        print_fail(reason)
    print_okblue(center_text('Press enter to continue',WIDTH))
    raw_input()


def show_document_screen(topic, document):
    cls_screen()
    show_title()
    show_break(1)
    show_topic_summary(topic)
    show_break(1)
    show_progress()
    show_line(WIDTH)
    show_break(1)
    show_document(document)
    show_break(1)
    show_line(WIDTH)
    show_break(1)
    
if __name__ == '__main__':
    import doctest
    doctest.testmod()
        