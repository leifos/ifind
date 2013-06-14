import os
import sys
import logging
import logging.config
import logging.handlers


def setup_event_logger(name='event.log', path=None):
    event_logger = logging.getLogger(name)
    event_logger.setLevel(logging.INFO)
    event_logger_handler = logging.FileHandler(os.path.join(path, name ) )
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    event_logger_handler.setFormatter(formatter)
    event_logger.addHandler(event_logger_handler)
    return event_logger

# TOPIC, (DOC, SNIP), DOCID, REL, TEXT_LEN, (VIEW, SKIP, REL, NONREL, UNSURE, ERR)

def log_event(event_logger, topic, text_type, docid, rel, char_len, text_len, action, seconds=0.0 ):
    msg = topic + ' '+ text_type + ' ' + str(docid) + ' ' + str(rel) + ' '+ str(char_len)+ ' '+ str(text_len)  + ' ' +  action + ' ' + str(seconds) 
    event_logger.info(msg) 
