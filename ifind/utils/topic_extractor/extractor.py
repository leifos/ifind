import os
import sys

"""
Simple topic extractor script - looks for a TREC topics file in list.txt.
Saves each topic to its own file, with the filename in the format 'topic.XXX', where XXX is the topic number.
Within the file, the first line makes up the title, with all remaining lines the description and narrative.
"""

def get_blank_topic():
    """
    Returns a blank topic dictionary.
    """
    return {'number': None, 'title': "", 'description': "", 'next_line': False}

def extract_topics(topic_filename):
    """
    Extracts topics from the source file (parameter topic_filename) and creates a file for each, with the title on the first line, and the description following.
    """
    source_file = open(topic_filename, 'r')
    topic_count = 0
    topics = []
    curr_topic = get_blank_topic()
    
    for line in source_file:
        line = line.strip()
        
        if line.startswith("<num> Number: "):
            curr_topic = get_blank_topic()
            topic_count = topic_count + 1
            topic_number = int(line[14:])
            
            curr_topic['number'] = topic_number
            
        elif line.startswith("<title>"):
            topic_title = line[8:]
            curr_topic['title'] = topic_title
            
            curr_topic['next_line'] = 'title'
        
        elif line.startswith("<desc>"):
            curr_topic['next_line'] = 'desc'
        
        elif line.startswith("<narr>"):
            curr_topic['next_line'] = 'narr'
            curr_topic['description'] = "{0}{1}{1}".format(curr_topic['description'], os.linesep)
        
        elif curr_topic['next_line'] in ['title', 'desc', 'narr']:
            if line.startswith("</top>"):
                curr_topic['next_line'] = False
                curr_topic['description'] = curr_topic['description'].strip()
                topics.append(curr_topic)
            
            elif curr_topic['next_line'] == 'title':
                curr_topic['title'] = "{0}{1} ".format(curr_topic['title'], line)
                curr_topic['title'] = curr_topic['title'].strip()
            elif curr_topic['next_line'] == 'desc':
                curr_topic['description'] = "{0}{1} ".format(curr_topic['description'], line)
            elif curr_topic['next_line'] == 'narr':
                curr_topic['description'] = "{0}{1} ".format(curr_topic['description'], line)
    
    save_topic_files(topics)
    source_file.close()

def save_topic_files(topics):
    """
    Given a list of topics, saves each to its own file.
    """
    for topic in topics:
        topic_number = topic['number']
        topic_title = topic['title']
        topic_description = topic['description']
        
        topic_file = open('topic.{0}'.format(topic_number), 'w')
        
        topic_file.write("{0}{1}{1}".format(topic_title, os.linesep))
        topic_file.write(topic_description)
        
        topic_file.close()
        print "Generated topic.{0}".format(topic_number)

def usage(script_name):
    """
    Prints the usage blurb out to stdout, and quits the program.
    """
    print "Usage:"
    print "{0} <TREC_TOPICS_FILE>".format(script_name)
    print "Assumes that <TREC_TOPICS_FILE> is a TREC Topics file as downloaded from http://trec.nist.gov/"
    sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 2:
        usage(sys.argv[0])
    
    extract_topics(sys.argv[1])