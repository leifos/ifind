import os

############
SPLIT_AT = '-'
DIRECTORY = os.path.abspath('baseline_informed_trec_topictitle')
BASE_FILENAME = 'informedtrecbaseline-{0}-informeduser.{1}'  # {0} corresponds to the topic, {1} to the type of output file.

LOG_DETAILS = ['TOTAL_QUERIES_ISSUED', 'TOTAL_SNIPPETS_EXAMINED', 'TOTAL_DOCUMENTS_EXAMINED', 'TOTAL_DOCUMENTS_MARKED_RELEVANT']
TREC_DETAILS = ['num_rel', 'num_ret', 'num_rel_ret', 'p5', 'p10', 'p20', 'map']
############

def get_topic_log_stats(topic, directory, base_filename):
    """
    Returns statistics recorded in the log file for a given topic.
    """
    log_file = base_filename.format(topic, 'log')
    log_file = os.path.join(directory, log_file)
    log_file = open(log_file, 'r')
    
    stats = {}
    
    for line in log_file:
        line = line.strip()
        line = line.split()
        
        if line[0] == 'INFO' and line[1] != 'SUMMARY':
            stats[line[1]] = int(line[2])
    
    log_file.close()
    return stats

def get_trec_eval_stats(topic, directory, base_filename):
    """
    Returns statistics recorded in the trec_eval output for the given topic.
    """
    log_file = base_filename.format(topic, 'out')
    log_file = os.path.join(directory, log_file)
    log_file = open(log_file, 'r')
    
    stats = {}
    
    for line in log_file:
        line = line.strip()
        line = line.split()
        
        stats[line[0].lower()] = line[2]
    
    log_file.close()
    return stats

def get_topics(directory, split_at='-'):
    """
    Returns a list of all the topics present in the given results directory.
    Splits filenames at split_at.
    """
    topics = []
    for filename in os.listdir(directory):
        filename = filename.split(split_at)
        
        topic = int(filename[1])
        
        if topic not in topics:
            topics.append(topic)
    
    return map(str, sorted(topics))

def get_headings_string():
    """
    Returns a CSV-formatted headings string for the output file.
    """
    return_str = "topic"
    
    for value in LOG_DETAILS:
        value = value.lower()
        return_str = "{0},{1}".format(return_str, value)
    
    for value in TREC_DETAILS:
        value = value.lower()
        return_str = "{0},{1}".format(return_str, value)
    
    return "{0}{1}".format(return_str, os.linesep)

def get_summary_string(topic, topic_details):
    return_str = "{0}".format(topic)
    
    for value in LOG_DETAILS:
        value = topic_details[topic]['stats'][value]
        return_str = "{0},{1}".format(return_str, value)
    
    for value in TREC_DETAILS:
        value = topic_details[topic]['trec_eval'][value]
        return_str = "{0},{1}".format(return_str, value)

    return "{0}{1}".format(return_str, os.linesep)
    
if __name__ == '__main__':
    topics = get_topics(DIRECTORY, SPLIT_AT)
    topic_details = {}
    
    summary_file = open('{0}.summary.csv'.format(DIRECTORY), 'w')
    summary_file.write(get_headings_string())
    
    for topic in topics:
        topic_details[topic] = {'stats': {}, 'trec_eval': {}}
        topic_details[topic]['stats'] = get_topic_log_stats(topic, DIRECTORY, BASE_FILENAME)
        topic_details[topic]['trec_eval'] = get_trec_eval_stats(topic, DIRECTORY, BASE_FILENAME)
        
        summary_file.write(get_summary_string(topic, topic_details))
        
    summary_file.close()
