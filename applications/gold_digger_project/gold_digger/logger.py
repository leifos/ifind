
import os
import logging

# create the logger once.

work_dir = os.getcwd()
log_file = os.path.join(work_dir, 'log_file2.log')
# create a logger by asking logging to get a logger called "event_log",
# if one exists it is returned, else a new logger called "event_log" is created

event_logger = logging.getLogger('event_log')

# set where the log is going to be written (here we use a file, could be a stream)
event_logger_handler = logging.FileHandler(log_file)

# configure the format of the message string for the logger
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
# set the formmater to the logger via a handler
event_logger_handler.setFormatter(formatter)
event_logger.addHandler(event_logger_handler)

# set the level of the messages we want to log and above  (DEBUG, INFO, WARNING, ERROR, CRITICAL)
event_logger.setLevel(logging.INFO)



# how to use externally,
# from logger_example import event_logger
# event_logger.info("an info message, perhaps to say a user issued a query")

# or once the event_log log is created you can (and should) ask for the logger by name,
#  and then log to it.
# test_logger = logging.getLogger("event_log")
# test_logger.info("a test msg")

# see also, https://docs.python.org/2/howto/logging.html
# and http://victorlin.me/posts/2012/08/26/good-logging-practice-in-python